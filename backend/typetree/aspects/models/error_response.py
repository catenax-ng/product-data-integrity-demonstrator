# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401
from typetree.aspects.models.error import Error


class ErrorResponse(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ErrorResponse - a model defined in OpenAPI

        error: The error of this ErrorResponse.
    """

    error: Error

ErrorResponse.update_forward_refs()