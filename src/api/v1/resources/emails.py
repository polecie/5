from fastapi import APIRouter, Depends, status

from src.api.v1.schemas.emails import EmailRequest, EmailResponse

__all__ = ("router",)

from src.services.email import EmailService, get_email_service

router = APIRouter(
    tags=["emails"],
)


@router.post(
    path="/users/{user_id}/emails",
    status_code=status.HTTP_201_CREATED,
    summary="Привязать почту к пользователю",
    response_model=EmailResponse
)
async def connect(
        user_id: int,
        data: EmailRequest,
        email_service: EmailService = Depends(get_email_service)
):
    return await email_service.create(data=data, user_id=user_id)


@router.delete(
    path="/users/{user_id}/emails/{email_id}",
    # status_code=status.HTTP_204_NO_CONTENT,
    summary="Отвязать почту от пользователя",
    response_model=dict
)
async def disconnect(
        user_id: int,
        email_id: int,
        email_service: EmailService = Depends(get_email_service)
):
    return await email_service.remove(email_id=email_id, user_id=user_id)


@router.get(
    path="/users/{user_id}/emails",
    status_code=status.HTTP_200_OK,
    summary="Получить список привязанных почт",
    response_model=list[EmailResponse]
)
async def get_many(
        user_id: int,
        email_service: EmailService = Depends(get_email_service),
):
    return await email_service.get_many(user_id=user_id)
