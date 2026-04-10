

from fastapi import APIRouter, HTTPException

from app.models.user import CreateUserRequest, UpdateUserRequest, UserResponse
from app.services.redis_service import RedisService
from app.services.user_service import UserService
from app.config.logging import logger

router = APIRouter(prefix="/users", tags=["Users"])
    

# create user
@router.post("/", response_model=UserResponse)
async def create_user(request: CreateUserRequest):
    logger.info(f"Received request to create user: {request}")
    try:
        user = await UserService.create_user(request)
        return user
    except Exception as e:
        # Handle the exception (e.g., log it, return an error response)
        raise e

# ---------------------------
# 🔹 GET USER
# ---------------------------
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    logger.info(f"Received request to get user with ID: {user_id}")
    cached_user = await RedisService.cache_get(user_id)
    if cached_user:
        logger.info(f"Cache hit for user_id: {user_id}")
        return UserResponse.model_validate(cached_user)

    logger.warn(f"Cache miss for user_id: {user_id}. Fetching from Redis...")
    user = await UserService.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Convert before caching
    await RedisService.cache_set(user_id, user.model_dump(mode="json"))  # Cache the user data as JSON-serializable dict

    return user


# ---------------------------
# 🔹 UPDATE USER
# ---------------------------
@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, request: UpdateUserRequest):
    logger.info(f"Received request to update user with ID: {user_id}, data: {request}")
    user = await UserService.update_user(user_id, request)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await RedisService.cache_set(user_id,  user.model_dump(mode="json"))  # Cache the updated user data

    return user

# ---------------------------
# 🔹 DELETE USER
# ---------------------------
@router.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: str):
    logger.info(f"Received request to delete user with ID: {user_id}")
    deleted = await UserService.delete_user(user_id)
    await RedisService.delete_cache(user_id)  # Remove the user from cache
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}