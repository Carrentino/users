from pydantic import BaseModel


class EmailNotification(BaseModel):
    to_user_email: str
    title: str
    body: str
