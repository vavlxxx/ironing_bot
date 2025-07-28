from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        exclude_unset=True,
        # str_min_length=1,
    )
