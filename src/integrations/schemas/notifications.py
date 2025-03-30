from pydantic import BaseModel


class EmailNotification(BaseModel):
    to_email: str
    title: str
    body: str
