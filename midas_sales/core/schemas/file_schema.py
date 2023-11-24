from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    name: str
    directory: str
    url_file: str | None


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    pass


class FileSchema(FileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
