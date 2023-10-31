from pydantic import BaseModel


class PostBase(BaseModel):
    room_id: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class PostOut(PostBase):
    id: int

    class Config:
        from_attributes = True
