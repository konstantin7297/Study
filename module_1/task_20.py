"""
Создайте декоратор access_control, который ограничивает доступ к функции на основе переданных ролей пользователя.
Декоратор должен принимать аргументы, определяющие допустимые роли (например, @access_control(roles=['admin', 'moderator'])).

Требования:
Если текущий пользователь имеет одну из допустимых ролей, функция выполняется.
Если нет, выбрасывается исключение PermissionError с соответствующим сообщением.
Реализуйте механизм определения текущей роли пользователя. Для целей задания можно использовать глобальную переменную или контекстный менеджер.
"""
import functools


class User:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role


def access_control(roles: list):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, User) and arg.role not in roles:
                    raise PermissionError(f'Denied {arg.name}')

            return func(*args, **kwargs)
        return wrapper
    return decorator


@access_control(roles=['admin'])
def test(user: User) -> str:
    return f'Access {user.name}'


for u in [
    User(name='first', role='admin'),
    User(name='second', role='moderator'),
]:
    print(test(u))
