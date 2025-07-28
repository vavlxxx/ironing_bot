

class InvalidPhoneNumberException(Exception):
    detail = "Некорректный номер телефона"

class ObjectNotFoundException(Exception):
    detail = "Объект не найден"

class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"

class OrderNotFoundException(ObjectNotFoundException):
    detail = "Заказ не найден"
