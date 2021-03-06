# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from .local_identifier_create import LocalIdentifierCreate, LocalIdentifierSearch
from digital_twin_registry.dependencies import MyBaseModel

class DigitalTwinBatch(MyBaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    DigitalTwinBatch - a model defined in OpenAPI

        identifiers: The identifiers of this DigitalTwinBatch.
    """

    identifiers: List[LocalIdentifierSearch]

DigitalTwinBatch.update_forward_refs()
