import datetime
import logging

import asyncpg


async def add_user(
    conn: asyncpg.Connection, name: str, date_of_birth: datetime.date
) -> int:
    # Insert a record into the created table.
    await conn.execute(
        """
        INSERT INTO users(name, dob) VALUES($1, $2)
    """,
        name,
        date_of_birth,
    )

    # Select a row from the table.
    row: asyncpg.Record = await conn.fetchrow(
        "SELECT * FROM users WHERE name = $1", "Bob"
    )
    # *row* now contains
    # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))
    return row["id"]
