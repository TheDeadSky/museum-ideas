from typing import TypedDict


class RegistrationData(TypedDict, total=True):
    name: str
    is_working_in_museum: bool
    museum: str | None
    scope_of_work: str | None
