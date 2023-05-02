from fastapi import APIRouter, Depends, status

from src.api.v1.schemas.users import UserRequest, UserResponse

__all__ = ("router",)

from src.services import UserService, get_user_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя",
    response_model=UserResponse
)
async def create(
        user: UserRequest,
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.create(user=user)


@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя по его id в телеграм",
    response_model=UserResponse
)
async def get_one(
        user_id: int,
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_one(user_id=user_id)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Получить список пользователей",
    response_model=list[UserResponse]
)
async def get_many(
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_many()
