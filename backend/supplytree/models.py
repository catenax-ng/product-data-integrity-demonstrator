# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

from typing import List, Optional, Union
from pydantic import BaseModel, AnyHttpUrl

class SupplyTreeUrlResponse(BaseModel):
    url: AnyHttpUrl

class UrlList(BaseModel):
    urls: List[AnyHttpUrl]

class DataNodeBase(BaseModel):
    url: AnyHttpUrl
    hash: Optional[str] = None
    hashMethod: Optional[str] = None
    type: Optional[str] = None

class Node(BaseModel):
    """ The lists can exist in pure URLs or objects describing the URL in detail """
    data: Union[List[AnyHttpUrl], List[DataNodeBase]] = []
    nodes: Union[List[AnyHttpUrl], List[DataNodeBase]] = []
    previous: Optional[Union[AnyHttpUrl, DataNodeBase]]

class NodeResponse(BaseModel):
    id: AnyHttpUrl
    node: Node
