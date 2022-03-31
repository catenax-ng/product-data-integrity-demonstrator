# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import Field
from .http_endpoint_create import HttpEndpointCreate
from .model_reference import ModelReference
from digital_twin_registry.dependencies import MyBaseModel


class AspectCreate(MyBaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    AspectCreate - a model defined in OpenAPI

        model_reference: The model_reference of this AspectCreate.
        http_endpoints: The http_endpoints of this AspectCreate.
    """

    model_reference: ModelReference = Field(None, alias='modelReference')
    http_endpoints: List[HttpEndpointCreate] = Field(None, alias='httpEndpoints')

AspectCreate.update_forward_refs()