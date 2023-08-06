import os
from importlib.machinery import SourceFileLoader
from pathlib import Path

import aiopg
import math
import typing
from dotenv import load_dotenv
from psycopg2 import sql, extras

from aiomigrator import queries, templates

ENV_MIGRATIONS_DIR_VARIABLE = "MIGRATIONS_DIR"
ENV_DB_VARIABLES = (
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
)
ENV_VARIABLES_TO_DSN = {
    "DB_HOST": "host",
    "DB_PORT": "port",
    "DB_NAME": "database",
    "DB_USER": "user",
    "DB_PASSWORD": "password",
}
INITIAL_VERSION = 0
VERSIONS_TABLE = sql.Identifier("versions")

load_dotenv()


async def init(migrations_dir: Path):
    cwd = os.getcwd()
    actual_dir = cwd / migrations_dir

    create_migrations_dir(actual_dir)
    create_env_file(cwd, actual_dir)
    await create_versions_table()


def create_migrations_dir(migrations_dir: Path):
    print(f"Trying to create migrations directory at: {migrations_dir}.")

    if migrations_dir.exists():
        if not migrations_dir.is_dir():
            raise NotADirectoryError(
                f"{migrations_dir} already exists and it is not a directory"
            )

        print("Migrations directory already exists.")
        return

    print("Successfully created migrations directory.")
    os.mkdir(migrations_dir)

    with open(migrations_dir / "__init__.py", "w") as file:
        file.write("")


def create_env_file(cwd: str, migrations_dir: Path):
    env_file_path = Path(cwd) / ".env"

    with open(env_file_path, "a") as env_file:
        variables_data = {
            variable: "" for variable in ENV_DB_VARIABLES if os.getenv(variable) is None
        }

        if os.getenv(ENV_MIGRATIONS_DIR_VARIABLE) is None:
            variables_data[ENV_MIGRATIONS_DIR_VARIABLE] = migrations_dir

        if variables_data:
            env_file.write("\n")

        for variable, value in variables_data.items():
            if os.getenv(variable) is None:
                env_file.write(f"{variable}={value}\n")

    print(
        ".env file updated. "
        "Please, fill variables starting with 'DB_', i.e. 'DB_HOST'"
    )


def use_db(func):
    dsn = {
        dsn_variable: os.getenv(env_variable)
        for env_variable, dsn_variable in ENV_VARIABLES_TO_DSN.items()
    }

    async def wrapper(
        *args,
        cursor: typing.Optional[aiopg.Cursor] = None,
        **kwargs,
    ):
        if cursor:
            return await func(cursor=cursor, *args, **kwargs)

        try:
            async with aiopg.create_pool(**dsn) as pool:  # TODO: reorganize dsn
                async with pool.acquire() as connection:
                    async with connection.cursor(
                        cursor_factory=extras.RealDictCursor
                    ) as cursor:
                        return await func(cursor=cursor, *args, **kwargs)

        except Exception as e:
            # TODO: handle
            print(f"Unknown exception raised while trying to use DB:\n{e}")

    return wrapper


@use_db
async def create_versions_table(cursor: aiopg.Cursor):
    await cursor.execute(
        queries.CREATE_MIGRATIONS_TABLE.format(versions_table=VERSIONS_TABLE),
        {"initial_version": INITIAL_VERSION},
    )
    result = await cursor.fetchall()

    assert (
        len(result) == 1
    ), "After versions table is created, there should be only one record inserted."

    version = result[0]
    assert (
        version["version"] == INITIAL_VERSION
    ), f"First version record should be equal to '{INITIAL_VERSION}'."


def _get_migrations_dir() -> Path:
    migrations_dir = os.getenv(ENV_MIGRATIONS_DIR_VARIABLE)

    if not migrations_dir:
        raise KeyError(f"'{ENV_MIGRATIONS_DIR_VARIABLE}' should be set.")

    return Path(migrations_dir).resolve()


def create_migration(version: int, name: str):
    migrations_dir = _get_migrations_dir()

    file_name = _get_file_name(version=version, name=name)

    file_path = migrations_dir / file_name
    if os.path.exists(file_path):
        raise FileExistsError(f"Migration file '{file_path}' already exists.")

    with open(file_path, "w") as file:
        file.write(templates.MIGRATION_TEMPLATE.format(version=version, name=name))


def _get_file_name(version: int, name: str):
    name_slug = "_".join(name.split())
    return f"{version:05}-{name_slug}.py"


@use_db
async def upgrade(
    target_version: typing.Optional[int] = None,
    cursor: aiopg.Cursor = None,
):
    current_version = await get_current_version(cursor=cursor)
    migrations_dir, migrations = get_migrations()

    if target_version is None:
        target_version = math.inf

    for migration in migrations:
        version, name, file_name = migration
        if current_version >= version:
            print(f"Version {version} ({name}) is already applied. Skipped.")
            continue

        if version > target_version:
            break

        migration_module = load_migration(str(migrations_dir / file_name))
        await migration_module.upgrade(cursor=cursor)

        await write_version(
            version=version,
            name=name,
            is_upgrade=True,
            cursor=cursor,
        )

        print(f"DB upgraded to version {version} ({name}).")


@use_db
async def downgrade(
    target_version: typing.Optional[int] = None,
    cursor: aiopg.Cursor = None,
):
    current_version = await get_current_version(cursor=cursor)
    migrations_dir, migrations = get_migrations()

    if target_version is None:
        target_version = 0

    for migration in migrations[::-1]:
        version, name, file_name = migration
        if current_version < version:
            print(f"Version {version} ({name}) is already reverted. Skipped.")
            continue

        if version <= target_version:
            break

        migration_module = load_migration(str(migrations_dir / file_name))
        await migration_module.downgrade(cursor=cursor)

        await write_version(
            version=version,
            name=name,
            is_upgrade=False,
            cursor=cursor,
        )

        print(f"DB downgraded from version {version} ({name}).")


@use_db
async def get_current_version(cursor: aiopg.Cursor = None) -> int:
    query = queries.SELECT_CURRENT_VERSION.format(versions_table=VERSIONS_TABLE)
    await cursor.execute(query)
    record = await cursor.fetchone()
    return record["version"]


@use_db
async def write_version(
    version: int,
    name: str,
    is_upgrade: bool,
    cursor: aiopg.Cursor = None,
):
    query = queries.INSERT_VERSION.format(versions_table=VERSIONS_TABLE)
    await cursor.execute(
        query,
        {
            "version": version,
            "name": name,
            "is_upgrade": is_upgrade,
        },
    )

    return await cursor.fetchall()


def get_migrations() -> typing.Tuple[Path, typing.List[typing.Tuple[int, str, str]]]:
    migrations_dir = _get_migrations_dir()

    migrations = sorted(
        [_parse_file_name(file_name) for file_name in os.listdir(str(migrations_dir))],
        key=lambda t: t[0],
    )
    return migrations_dir, migrations


def load_migration(file_name: str):
    loader = SourceFileLoader("migration", file_name)
    return loader.load_module()


def _parse_file_name(file_name: str) -> typing.Tuple[int, str, str]:
    version_str, name = file_name.rsplit(".", maxsplit=1,)[0].split(
        "-",
        maxsplit=1,
    )  # TODO: update

    return int(version_str), name, file_name
