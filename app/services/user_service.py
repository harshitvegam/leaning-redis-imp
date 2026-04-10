from datetime import datetime
from typing import Optional

from app.producer.stream import publish_user_created
from app.services.redis_service import RedisService
from app.models.user import CreateUserRequest, UpdateUserRequest, UserResponse


class UserService:

    KEY_PREFIX = "user"

    # ---------------------------
    # 🔹 GENERATE USER ID
    # ---------------------------
    @staticmethod
    async def _generate_user_id() -> str:
        user_id = await RedisService.increment("metric:users:id")
        print(f"Generated user ID: {user_id}")
        return str(user_id)

    # ---------------------------
    # 🔹 CREATE USER
    # ---------------------------
    @staticmethod
    async def create_user(data: CreateUserRequest) -> UserResponse:
        user_id = await UserService._generate_user_id()

        user_key = f"{UserService.KEY_PREFIX}:{user_id}"
        print(f"Creating user with key: {user_key}")
        user_data = {
            "user_id": user_id,
            "name": data.name,
            "email": data.email,
            "number": data.number,
            "created_at": datetime.utcnow().isoformat()
        }

        await RedisService.set_json(user_key, user_data)
        print(f"User created in Redis: {user_data}")
        print(" user data ",type(user_data), user_data)
        await publish_user_created(user_data)
        print(f"Published user created event for user_id: {user_id}")
        # metric
        await RedisService.increment("metric:users:created")

        return UserResponse(**user_data)

    # ---------------------------
    # 🔹 GET USER
    # ---------------------------
    @staticmethod
    async def get_user(user_id: str) -> Optional[UserResponse]:
        user_key = f"{UserService.KEY_PREFIX}:{user_id}"

        data = await RedisService.get_json(user_key)

        if not data:
            return None

        return UserResponse(**data)

    # ---------------------------
    # 🔹 UPDATE USER
    # ---------------------------
    @staticmethod
    async def update_user(
        user_id: str,
        updates: UpdateUserRequest
    ) -> Optional[UserResponse]:

        user_key = f"{UserService.KEY_PREFIX}:{user_id}"

        existing = await RedisService.get_json(user_key)
        if not existing:
            return None

        update_data = updates.model_dump(exclude_none=True)

        updated = await RedisService.update_json(user_key, update_data)

        await RedisService.increment("metric:users:updated")

        return UserResponse(**updated)

    # ---------------------------
    # 🔹 DELETE USER
    # ---------------------------
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        user_key = f"{UserService.KEY_PREFIX}:{user_id}"

        existing = await RedisService.get_json(user_key)
        if not existing:
            return False

        await RedisService.delete_json(user_key)

        await RedisService.increment("metric:users:deleted")

        return True