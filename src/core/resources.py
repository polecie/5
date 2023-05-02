from enum import Enum


class ApiResources(Enum):
    prefix: str = "/api/v1"  # префикс для всех урлов
    docs: str = "/api/v1/openapi"  # адрес документации
    root: str = "/"  # адрес для корневого урла

    # адреса для ресурсов
    users: str = "/users/{}"
    senders: str = "/senders/{}"
    emails: str = "/emails/{}"
    providers: str = "/providers/{}"
