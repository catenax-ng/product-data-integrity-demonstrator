# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401
from digital_twin_registry.dependencies import MyBaseModel


class ModelReference(MyBaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ModelReference - a model defined in OpenAPI

        urn: The urn of this ModelReference.
    """

    urn: str

    @validator("urn")
    def urn_min_length(cls, value):
        assert len(value) >= 5
        return value

    @validator("urn")
    def urn_max_length(cls, value):
        assert len(value) <= 100
        return value

ModelReference.update_forward_refs()
