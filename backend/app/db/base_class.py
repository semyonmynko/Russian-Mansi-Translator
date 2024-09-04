import typing as t
import re

from sqlalchemy.ext.declarative import as_declarative, declared_attr


class_registry: t.Dict = {}

def camel_to_snake(name):
    """
    Преобразует строку из CamelCase в snake_case.
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Генерирует имя таблицы на основе имени класса,
        преобразуя его из CamelCase в snake_case.
        """
        return camel_to_snake(cls.__name__)