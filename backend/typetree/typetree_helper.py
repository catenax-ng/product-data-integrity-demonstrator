# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import json
import requests
from supplytree.supplytreee_helper import get_data_with_type_from_node, parse_data_from_url, parse_node_from_url
from .dependencies import ITEMTYPE_TYPE
from .models import ItemType
from .dependencies import DT_TWIN_REGISTRY, TYPETREE_BASE_URL
from digital_twin_registry.models.aspect_create import AspectCreate
from digital_twin_registry.models.digital_twin_create import DigitalTwinCreate, DigitalTwinCreateList
from digital_twin_registry.models.digital_twin import DigitalTwin
from digital_twin_registry.models.http_endpoint_create import HttpEndpointCreate
from digital_twin_registry.models.http_method import HttpMethod
from digital_twin_registry.models.local_identifier_create import LocalIdentifierCreate
from digital_twin_registry.models.model_reference import ModelReference

class MultipleTypeInformationException(Exception):
    pass


def get_type_data_from_node_url(node_url: str, tenant: str, fetch_child_type_data=False):
    """
    Starting point often is a Node URL. This is a helper to easily get the type data from that.

    Raises an MultipleTypeInformationException if the node contains more than 1 type information entry - which is not allowed per definition.

    Returns None if doesn't contain any.
    """
    node = parse_node_from_url(node_url, tenant=tenant)
    type_data_urls = get_data_with_type_from_node(node, ITEMTYPE_TYPE)
    if len(type_data_urls) > 1:
      raise MultipleTypeInformationException
    
    if len(type_data_urls) == 1:
        data = parse_data_from_url(str(type_data_urls[0]), tenant=tenant)
        item_type = ItemType.parse_obj(data)
        data = {"type_data": item_type}
        if fetch_child_type_data:
            child_types_data = {}
            for child in item_type.child_types:
                d = get_type_data_from_node_url(str(child), tenant=tenant)
                child_types_data[str(child)] = d
            data['child_types_data'] = child_types_data

        return data

    return None

def register_type_twin(node_id: str, tenant: str) -> DigitalTwin:
    type_data = ItemType.parse_obj(get_type_data_from_node_url(node_id, tenant=tenant)['type_data'])
    id = type_data.catena_x_unique_id
    part_aspect_url = TYPETREE_BASE_URL + "/parttypetwin/" + id
    relationship_aspect_url = TYPETREE_BASE_URL + "/relationship/" + id

    twin_create = DigitalTwinCreate(id=id, description="", manufacturer="XYZ",
    local_identifiers=[
        LocalIdentifierCreate(key="type_name", value=type_data.type_name),
        LocalIdentifierCreate(key="part_name", value=type_data.part_name),
        LocalIdentifierCreate(key="part_name_customer", value=type_data.part_name_customer)
    ], aspects=[
        AspectCreate(model_reference=ModelReference(urn="urn:bamm:com.catenaX:0.1.0#PartTypization"), http_endpoints=[
            HttpEndpointCreate(method=HttpMethod.get, url=part_aspect_url)
        ]),
        AspectCreate(model_reference=ModelReference(urn="urn:bamm:com.catenaX:0.1.1#AssemblyPartRelationship"), http_endpoints=[
            HttpEndpointCreate(method=HttpMethod.get, url=relationship_aspect_url)
        ])
    ])

    twin_list = DigitalTwinCreateList(__root__=[
        twin_create
    ])

    data = twin_create.dict(by_alias=True)

    myj = [data]
    print(myj)
    r = requests.post(DT_TWIN_REGISTRY + "/twins", json=myj)
    print(r.content)
    j = r.json()
    twin = DigitalTwin.parse_obj(j[0]) # we add 1, so we expect also only 1 elment in the list
    return twin
