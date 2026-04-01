from typing import TypedDict
class State(TypedDict):
    question: str
    schema: str
    sql: str
    result: str
    error: str