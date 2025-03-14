from pydantic import BaseModel


class EmailNotification(BaseModel):
    email: str
    title: str
    body: str
