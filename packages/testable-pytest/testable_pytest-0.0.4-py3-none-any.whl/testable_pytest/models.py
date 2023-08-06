from pydantic import BaseModel


class Case(BaseModel):
    """
    Testable test case structure
    """
    name: str | None = None
    owner: str | None = None
