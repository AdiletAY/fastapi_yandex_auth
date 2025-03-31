from humps import camelize
from pydantic import BaseModel as _BaseModel


class BaseSchema(_BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "alias_generator": camelize,
    }
