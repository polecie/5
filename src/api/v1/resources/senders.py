from fastapi import APIRouter, Depends, status

from src.api.v1.schemas.senders import SenderRequest, SenderResponse

__all__ = ("router",)

from src.services.sender import SenderService, get_sender_service

router = APIRouter(
    tags=["senders"]
)


@router.post(
    path="/users/{user_id}/senders",
    status_code=status.HTTP_201_CREATED,
    summary="Привязать отправителя к пользователю",
    response_model=SenderResponse
)
async def connect(
        user_id: int,
        data: SenderRequest,
        sender_service: SenderService = Depends(get_sender_service),
):
    return await sender_service.create(data=data, user_id=user_id)


@router.delete(
    path="/users/{user_id}/senders/{sender_id}",
    # status_code=status.HTTP_204_NO_CONTENT,
    summary="Отвязать отправителя от пользователя",
    response_model=dict
)
async def disconnect(user_id: int, sender_id: int, sender_service: SenderService = Depends(get_sender_service)):
    return await sender_service.remove(sender_id=sender_id, user_id=user_id)


@router.get(
    path="/users/{user_id}/senders",
    status_code=status.HTTP_200_OK,
    summary="Получить список привязанных отправителей",
    response_model=list[SenderResponse]
)
async def get_many(user_id: int, sender_service: SenderService = Depends(get_sender_service)):
    return await sender_service.get_many(user_id=user_id)
