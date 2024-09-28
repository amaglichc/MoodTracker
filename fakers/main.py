from faker import Faker
from db.repositories.UserRepo import save_user
from Schemas.UserSchema import SignUpSchema


faker = Faker()


async def fill():
    for _ in range(1000):
        await save_user(
            SignUpSchema(
                username=faker.user_name(),
                email=faker.email(),
                password=faker.password(),
            )
        )
