import os
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from ..models.db_models import Base, ChildParent, ChildTutor, User
from ..models.request_models import RegUser

db_url = os.getenv("DATABASE_URL")

engine = create_async_engine(db_url)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)


@asynccontextmanager
async def async_session_scope():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()


async def initialize_db(username, password):
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(f"Error initializing database: {e}")

    admin = RegUser(email=username, password=password, role="admin")
    try:
        await create_user(admin)

        await get_user(username)
        print("User created successfully.")
    except Exception as e:
        print(f"Error creating admin user: {e}")


async def create_user(user: RegUser):

    async with async_session_scope() as session:

        user_exist = await session.execute(
            select(User).filter(User.email == user.email)
        )
        if user_exist.scalar() is None:
            new_user = User(
                first_name=user.first_name,
                second_name=user.second_name,
                phone_number=user.phone_number,
                email=user.email,
                hashed_password=user.password,
                role=user.role,
            )
            session.add(new_user)
            return 1
        return -1


def user_to_dict(user: User):
    return RegUser(
        user_id=user.user_id,
        email=user.email,
        password=user.hashed_password,
        phone_number=user.phone_number,
        first_name=user.phone_number,
        second_name=user.second_name,
        role=user.role,
    )


async def get_tutors():
    async with async_session_scope() as session:
        tutors = await session.execute(select(User).filter(User.role == "tutor"))
        tutors_list = tutors.scalars().all()
        if tutors_list:
            return [user_to_dict(tutor) for tutor in tutors_list]
        return []


async def get_user(email: str):
    async with async_session_scope() as session:
        user = await session.execute(select(User).filter(User.email == email))
        user_obj = user.scalar()
        if user_obj:
            return user_to_dict(user_obj)
        return None


async def create_student(child: RegUser, parent_email: str):
    async with async_session_scope() as session:
        creation_res = await create_user(child)

        db_child = await get_user(child.email)
        db_parent = await get_user(parent_email)

        if creation_res:
            record = ChildParent(
                child_id=db_child.user_id,
                parent_id=db_parent.user_id,
                is_approoved=True,
            )
            session.add(record)
            return 1
        return -1
    

async def offer_student(user: RegUser, tutor_email: str):
    async with async_session_scope() as session:
        if user.role == "child":
            
            db_child = await get_user(user.email)
            if not db_child:
                return -2
            
            db_tutor = await get_user(tutor_email)
            if not db_tutor:
                return -1

            record = ChildTutor(
                child_id=db_child.user_id,
                tutor_id=db_tutor.user_id,
                is_approoved=False
            )

            session.add(record)

            return 1
        
        db_parent = await get_user(user.email)
        db_tutor = await get_user(tutor_email)

        if not db_tutor:
            return -1

        db_child = user_to_dict(session.execute(select(ChildParent).where(parent_id=db_parent.user_id).first()))

        if not db_child:
            return -2

        record = ChildTutor(
                child_id=db_child.user_id,
                tutor_id=db_tutor.user_id,
                is_approoved=False
            )
        session.add(record)

        return 1


async def get_all_users() -> list:
    async with async_session_scope() as session:
        users = await session.execute(select(User))
        users_list = users.scalars().all()
        if users_list:
            return [user_to_dict(user) for user in users_list]
        return []
