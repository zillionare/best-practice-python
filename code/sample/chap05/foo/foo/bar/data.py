import asyncio

from gino import Gino

db = Gino()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(), default="noname")
    dob = db.Column(db.Date(), nullable=False)


async def main():
    await db.set_bind("postgresql://zillionare:123456@localhost/bpp")
    await db.gino.create_all()

    # further code goes here

    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())
