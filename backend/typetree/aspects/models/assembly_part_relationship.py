# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401
from pydantic import Field
from typetree.dependencies import SchemaConfig
from typetree.aspects.models.urn_bamm_com_catenax_traceability011_setof_child_ids_characteristic_child import UrnBammComCatenaxTraceability011SetofChildIdsCharacteristicChild


class AssemblyPartRelationship(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    AssemblyPartRelationship - a model defined in OpenAPI

        catena_x_unique_id: The catena_x_unique_id of this AssemblyPartRelationship.
        child_collection: The child_collection of this AssemblyPartRelationship.
    """

    catena_x_unique_id: str = Field([], alias='catenaXUniqueId')
    child_parts: Optional[List[UrnBammComCatenaxTraceability011SetofChildIdsCharacteristicChild]] = Field([], alias='childParts')

    class Config(SchemaConfig):
        ...

    """
    @validator("catena_x_unique_id")
    def catena_x_unique_id_pattern(cls, value):
        assert value is not None and re.match(r"^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}$", value)
        return value
    """

AssemblyPartRelationship.update_forward_refs()
