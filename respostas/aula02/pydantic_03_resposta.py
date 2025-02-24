from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated, Any

from pydantic import AfterValidator, BaseModel, BeforeValidator, model_validator


class Gender(str, Enum):
    MALE = 'masculino'
    FEMALE = 'feminino'
    NOT_INFORMED = 'prefiro nao informar'
    OTHER = 'outro'


def string_has_content(value: str) -> str:
    if len(value) == 0:
        raise ValueError('Strings vazias não são permitidas')

    return value


def starts_with_upper_case(value: str) -> str:
    if not value[0].isupper():
        raise ValueError(f"'{value}' precisa iniciar com uma letra maiúscula")

    return value


def formatted_cpf(cpf: str) -> str:
    n1, n2, n3_n4 = cpf.split('.')
    n3, n4 = n3_n4.split('-')

    if len(n1) != 3 or len(n2) != 3 or len(n3) != 3 or len(n4) != 2:
        raise ValueError('O CPF precisa seguir o seguinte formato: 000.000.000-00')

    try:
        int(n1), int(n2), int(n3), int(n4)
    except ValueError:
        raise ValueError('O CPF precisa ser apenas composto por números no formato 000.000.000-00')

    return cpf


def valid_email(email: str) -> str:
    if '@' not in email:
        raise ValueError('O e-mail deve conter um caractere de @')

    user, domain = email.split('@')

    if len(user) == 0 or len(domain) == 0:
        raise ValueError(
            'O e-mail deve conter um nome de usuário e um domínio. ex: user@domain.com'
        )

    return email


def valid_password(password: str) -> str:
    # no mínimo 8 dígitos e se no conteúdo há 3 números, 1 caractere especial e uma letra maiúscula
    if len(password) < 8:
        raise ValueError('A senha deve conter pelo menos 8 caracteres')

    upper_chars = [char for char in password if char.isupper()]
    if len(upper_chars) < 1:
        raise ValueError('A senha deve conter pelo menos uma letra maiúscula')

    digits_chars = [char for char in password if char.isdigit()]
    if len(digits_chars) < 3:
        raise ValueError('A senha deve conter pelo menos 3 números')

    special_chars = [char for char in password if not char.isdigit() and not char.isalpha()]
    if len(special_chars) < 1:
        raise ValueError('A senha deve conter pelo menos 1 caractere especial')

    return password


def valid_date(date_value: Any) -> datetime:
    if isinstance(date_value, str):
        return datetime.strptime(date_value, '%d/%m/%Y')
    else:
        return date_value


class Person(BaseModel):
    nome: Annotated[str, AfterValidator(string_has_content), AfterValidator(starts_with_upper_case)]
    cpf: Annotated[str, AfterValidator(string_has_content), AfterValidator(formatted_cpf)]
    genero: Gender
    email: Annotated[str, AfterValidator(string_has_content), AfterValidator(valid_email)]
    senha: Annotated[str, AfterValidator(string_has_content), AfterValidator(valid_password)]
    confirmaSenha: Annotated[
        str, AfterValidator(string_has_content), AfterValidator(valid_password)
    ]
    dataNascimento: Annotated[str | datetime, BeforeValidator(valid_date)]

    @model_validator(mode='after')
    def check_passwords_match(self) -> Person:
        if self.senha != self.confirmaSenha:
            raise ValueError('As senhas devem ser iguais!')

        return self


if __name__ == '__main__':
    person = Person(
        nome='Joao canhoto',
        cpf='000.000.000-00',
        genero=Gender.MALE,
        email='joao@cesar.school',
        senha='Next@2025',
        confirmaSenha='Next@2025',
        dataNascimento='16/07/1951',
    )
    print(person)
