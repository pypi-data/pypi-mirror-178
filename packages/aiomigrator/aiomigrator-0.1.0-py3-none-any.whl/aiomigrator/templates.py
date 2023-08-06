MIGRATION_TEMPLATE = """from aiopg import Cursor

version = "{version}"
name = "{name}"


async def upgrade(cursor: Cursor):
    query = "select 1"  # your code here
    await cursor.execute(query)


async def downgrade(cursor: Cursor):
    query = "select 1"  # your code here
    await cursor.execute(query)
"""
