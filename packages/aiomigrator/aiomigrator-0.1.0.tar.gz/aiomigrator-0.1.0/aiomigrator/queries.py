from psycopg2 import sql

CREATE_MIGRATIONS_TABLE = sql.SQL(
    """
    create table if not exists {versions_table}
    (
        id           serial primary key,
        version      integer not null,
        name         text    not null default '',
        is_upgrade   bool             default true,
        applied_date timestamp        default now()
    );
    
    insert into {versions_table} (version, name)
    values (%(initial_version)s, 'initial_migration')
    on conflict do nothing
    returning *;
"""
)


SELECT_CURRENT_VERSION = sql.SQL(
    "select * from {versions_table} order by applied_date desc limit 1;"
)

INSERT_VERSION = sql.SQL(
    """
    insert into {versions_table}
    (version, name, is_upgrade) 
    values (%(version)s, %(name)s, %(is_upgrade)s)
    returning *;
    """
)
