# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, AnyHttpUrl

from supplytree.models import DataNodeBase, Node, NodeResponse
from .aspects.models.part_typization import PartTypization

class SchemaConfig:
    """
    Pydantic model configuration
    """
    allow_population_by_field_name = True

class Theme(BaseModel):
    primary: str = '#1976D2'
    secondary: str = '#424242'
    accent: str = '#82B1FF'
    error: str = '#FF5252'
    info: str = '#2196F3'
    success: str = '#4CAF50'
    warning: str = '#FFC107'

class ConfigPost(BaseModel):
    theme: Theme = Theme()
    organization_name = ''

    class Config(SchemaConfig):
        ...

class Co2Data(BaseModel):
    co2: str = ''

class MultipleCo2InformationException(Exception):
    pass


class ItemType(PartTypization):
    #id: AnyHttpUrl
    type_name: str
    # version: Optional[str]
    #child_types: List['ItemType'] = []
    child_types: List[AnyHttpUrl] = []
ItemType.update_forward_refs()

class TypeNameList(BaseModel):
    type_names: List[str] = []

class ItemTypeUrlDetails(BaseModel):
    #id: Union[AnyHttpUrl, DataNodeBase]
    type_details: ItemType
    node: Optional[NodeResponse]

class ItemTypeWithPrevious(BaseModel):
    previous: Optional[AnyHttpUrl]
    type_details: ItemType
    co2_details: Co2Data = None

class TypeNameListDetails(BaseModel):
    data: Dict[str, ItemTypeUrlDetails] = {}

class Co2(BaseModel):
    co2: float
    unit: str

