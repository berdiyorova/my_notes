from app.models import UserModel, Base
from app.database import engine, get_db


class UserService:
    # Baza yaratish (agar mavjud bo'lmasa)
    Base.metadata.create_all(bind=engine)
    db = next(get_db())  # Sessiya yaratish


    async def create_user(self, username: str, password: str):
        new_user = UserModel(username=username, password=password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    # Foydalanuvchi olish
    async def get_user(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    # Foydalanuvchilar ro'yxatini olish
    async def get_users(self, page: int = 1, limit: int = 10):
        skip = (page - 1) * limit

        return self.db.query(UserModel).offset(skip).limit(limit).all()

    # Foydalanuvchi ma'lumotlarini yangilash
    async def update_user(self, user_id: int, username: str = None, password: str = None):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None  # Foydalanuvchi topilmadi

        if username:
            user.username = username
        # if password:
        #     user.password = await get_password_hash(password)

        self.db.commit()
        self.db.refresh(user)
        return user


    async def get_user_by_username(self, username: str) -> None | UserModel:
        user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return user if user else None

