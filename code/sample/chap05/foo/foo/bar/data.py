import asyncio
import datetime

from gino import Gino

db = Gino()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(), default="noname")
    dob = db.Column(db.Date(), nullable=False)


async def main():
    await db.set_bind("postgresql://zillionare:123456@localhost/pbp")
    await db.gino.create_all()

    # 其它功能代码
    await User.create(name="zillionare", dob=datetime.date(2024,1,1))

    # select * from users
    users = await User.query.gino.all()
    print(users[0].name, users[0].dob)
    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())
