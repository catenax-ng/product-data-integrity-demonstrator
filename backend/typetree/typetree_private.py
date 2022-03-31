# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import base64
import os
from uuid import uuid4
from datetime import date
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic.networks import AnyHttpUrl

from .typetree_helper import get_type_data_from_node_url, register_type_twin

from supplytree.supplytreee_helper import parse_data_from_url, parse_node_from_file, parse_node_from_url
from .dependencies import ITEMTYPE_TYPE
from .models import Co2Data, ConfigPost, ItemType, ItemTypeUrlDetails, ItemTypeWithPrevious, TypeNameList, TypeNameListDetails
from supplytree.models import DataNodeBase, SupplyTreeUrlResponse
from supplytree.supplytree_private import *
from supplytree.supplytree_public import *
from supplytree.supplytreee_helper import *
from .co2 import get_co2_data_from_node_url
import shelve
from .dependencies import *

router = APIRouter(tags=['TypeTree Private'])

@router.get('/{tenant}/type/{type_name}/head')
def get_type_head(type_name: str, tenant: str):
    """
    Returns the latest node reference URL that is currently known to the system.
    """
    with shelve.open(get_db_name_base(tenant=tenant), 'r') as db:
        if not type_name in db:
            raise HTTPException(status_code=404, detail="Could not find any item for type_name: " + type_name)
        return SupplyTreeUrlResponse(url=db[type_name])

@router.get('/{tenant}/type/by-name/{type_name}')
def get_type_details(type_name: str, tenant: str):
    """
    Get type details for a given type_name
    """
    with shelve.open(get_db_name_base(tenant=tenant), 'r') as db:
        node_url = db[type_name]
        type_data = get_type_data_from_node_url(node_url, tenant=tenant)['type_data']
        return type_data

@router.get('/{tenant}/type/by-node-id/{node_id}')
def get_type_by_node_id(node_id: str, tenant: str):
    """
    Get details by a given Node ID / Link / URL.
    Since it's part of the path, it needs to be base64url encoded
    """
    url = decode_base64urlencoded(node_id)
    type_data = get_type_data_from_node_url(url, tenant=tenant, fetch_child_type_data=True)
    co2_data = get_co2_data_from_node_url(url, tenant=tenant)
    type_data['co2_data'] = co2_data
    is_remote = is_remote_node(url, tenant=tenant)
    type_data['meta'] = {
        'node_id': url,
        'is_remote_type': is_remote
    }
    # additionally to support the attestation request we need some more meta data - should be somewhere else in the future
    node = parse_node_from_url(url, tenant=tenant)
    for d in node.data:
        if d.type == ITEMTYPE_TYPE:
            type_data['meta']['type'] = d.type
            type_data['meta']['data_id'] = str(d.url)


    return type_data

@router.get('/{tenant}/type/new_versions/by-node-id/{node_id}')
def get_new_versions(node_id: str, tenant: str):
    """
    """
    url = decode_base64urlencoded(node_id)
    return get_newer_versions(url, tenant=tenant)


@router.post('/{tenant}/type/details-by-name')
async def type_details_by_name(type_names: TypeNameList, tenant: str) -> TypeNameListDetails:
    result = TypeNameListDetails()
    for type_name in type_names.type_names:
        url = get_type_head(type_name, tenant=tenant).url
        # read the corresponding node object
        n = parse_node_from_url(url, tenant=tenant)
        # find from "data" section the one with the type of type information
        for d in n.data:
            # TODO: check if structure contains "hash" attribute... (might change supplytree helper functions...)
            if d.type == ITEMTYPE_TYPE:
                # parse into json
                data = parse_data_from_url(d.url, tenant=tenant)
                item_type = ItemType.parse_obj(data)
                # add to the result
                result.data[type_name] = ItemTypeUrlDetails(id=d, type_details=item_type, node=NodeResponse(id=url, node=n))
            else:
                # TODO: check all data? rather not, assuming we don't have proper type information available
                pass
    return result

@router.get('/{tenant}/types')
async def get_types(tenant: str) -> TypeNameListDetails:
    try:
        with shelve.open(get_db_name_base(tenant=tenant), 'r') as db:
            types_list = TypeNameList
            keys = list(db.keys())
            types_list.type_names = keys
            return await type_details_by_name(type_names=types_list, tenant=tenant)
    except:
        pass
    return TypeNameListDetails()


async def upsert(item_type: ItemType, tenant: str, previous: str = '', co2: Co2Data = None) -> NodeResponse:
    # create node object
    node = Node()

    # insert new data object
    if previous:
        prev_version = get_type_data_from_node_url(previous, tenant=tenant)
        item_type.catena_x_unique_id = prev_version['type_data'].catena_x_unique_id
    else:
        # a newely created type, that means we set the "created_on" prop
        today = date.today()
        item_type.created_on = str(today)
        id = str(uuid4())
        item_type.catena_x_unique_id = id
        # TODO: register unique identifier on a registry and discovery service
    
    item_type.modified_on = str(date.today())
    # fill duplicate elements
    if not item_type.part_name:
        item_type.part_name = item_type.type_name
    if not item_type.part_name_customer:
        item_type.part_name_customer = item_type.type_name
    
    data_url = await post_data(tenant=tenant, content=item_type.dict())
    data_object = DataNodeBase(
        url=data_url.url,
        type=ITEMTYPE_TYPE
    )
    node.data.append(data_object)

    #... and for CO2
    if co2:
        co2_data_url = await post_data(tenant=tenant, content=co2.dict())
        co2_object = DataNodeBase(
            url=co2_data_url.url,
            type=CO2_TYPE
        )
        node.data.append(co2_object)

    node.nodes = item_type.child_types
    
    if previous:
        # update with reference to the previous
        node.previous = previous


    node_r = await post_node(node=node, tenant=tenant)

    return node_r

@router.post("/{tenant}/ItemType")
async def post_item_type(item: ItemTypeWithPrevious, tenant: str) -> ItemTypeUrlDetails:
    """
    If 'previous' is set, we consider it an update on top of that.

    If not, the internal database is checkd for a potentially existing version that is being used.

    If not, a new item is created.

    TODO: Force new creation?
    """
    result = None
    item_type = item.type_details
    co2 = item.co2_details
    if len(item_type.type_name) < 1:
      raise HTTPException(500, "type_name must contain at least 1 character.")
    with shelve.open(get_db_name_base(tenant=tenant)) as db:
        update_case = item_type.type_name in db or 'previous' in item
        if update_case:
            # it is an update case
            # TODO: conflicts?
            # 'previous' field is considered more important than our database information!
            previous = None
            if item.previous:
                previous = str(item.previous)
            elif item_type.type_name in db:
                previous = db[item_type.type_name]
            node_response = await upsert(item_type, tenant=tenant, previous=previous, co2=co2)
        else:
            # insert case
            node_response = await upsert(item_type, tenant=tenant, co2=co2)

        db[item_type.type_name] = str(node_response.id)
        result = ItemTypeUrlDetails(node = node_response, type_details=item_type)
    # update uuid mapping table
    updated_type = ItemType.parse_obj(get_type_data_from_node_url(str(node_response.id), tenant=tenant)['type_data'])
    with shelve.open(get_db_name_uuid_heads(tenant=tenant)) as db:
        db[updated_type.catena_x_unique_id] = str(node_response.id)

    if not update_case:
        # a new type has been created, so let's register the twin for it
        if DT_TWIN_REGISTRY:
            twin = register_type_twin(str(node_response.id), tenant=tenant)
            print(twin)
        else:
            print("NOT createing a twin. Missing env: DT_TWIN_REGISTRY")

    return result

@router.post('/{tenant}/ItemType/by-link')
async def post_item_type_by_link(input_url: SupplyTreeUrlResponse, tenant: str) -> ItemTypeUrlDetails:
    """
    From a given Node URL, we fetch the node, parse for data objects that contain type information,
    fetch the data object, parse it and return it.

    Every type added "by-link" is considered a "remote type", meaning one from our suppliers. We track them separately for updates.
    """
    url = input_url.url
    r = await post_references(UrlList(urls=[url]), tenant=tenant)
    node = parse_node_from_url(url, tenant=tenant)
    type_data_urls = get_data_with_type_from_node(node, ITEMTYPE_TYPE)
    if len(type_data_urls) != 1:
        raise HTTPException(500, "Given node does not contain exactly 1 type information object ({0})".format(ITEMTYPE_TYPE))

    data = parse_data_from_url(type_data_urls[0], tenant=tenant)
    item_type = ItemType.parse_obj(data)
    with shelve.open(get_db_name_base(tenant=tenant)) as db:
        db[item_type.type_name] = str(url)
    with shelve.open(get_db_name_remote_types(tenant=tenant)) as db:
        db[item_type.type_name] = str(url)

    response = ItemTypeUrlDetails(
        type_details=item_type, node=NodeResponse(id=url, node=node))

    return response

@router.get('/{tenant}/ItemType/remotes')
async def get_remote_types(tenant: str):
    """
    Returns a list of all "remote" types (types that we added by link).

    Fetches remote systems for updates for those types.

    Result contains a list of newer "Node ID / Links" and the according type information data (same ordering, latest version at the end).

    Result also contains a list of type_names (updated_type_names) of types which actually received an update. Makes it easier to access
    just those from the list/dict
    """
    result = {"remote_types": {} }
    updated_type_names = []
    with shelve.open(get_db_name_remote_types(tenant=tenant), 'r') as db:
        for type_name in db:
            url = db[type_name]
            newer_versions_data = get_newer_versions(url, tenant=tenant)
            if newer_versions_data['newer_versions']:
                updated_type_names.append(type_name)

            result['remote_types'][type_name] = newer_versions_data
    result['upated_type_names'] = updated_type_names # to easier find out what got an update. Can be used to only access those types from the list
    return result

def get_newer_versions(node_id:str, tenant: str):
    """
    Internal function to build the result for e.g. get_remote_types()
    """
    url = node_id
    current_type_data = get_type_data_from_node_url(url, tenant=tenant)['type_data'] #TODO: catch exception
    newer_versions = find_latest_version(url, tenant=tenant)
    updated_types = []
    for node_url in newer_versions:
        # seems ther are remote updates on that type
        type_data = get_type_data_from_node_url(node_url, tenant=tenant)['type_data'] #TODO: catch exception
        updated_types.append(type_data)

    result = {
        "type_name": current_type_data.type_name,
        "current_data": current_type_data,
        "newer_versions": newer_versions,
        "newer_versions_data": updated_types
    }
    return result



@router.get('/{tenant}/graph/{b64_node_id}')
def get_graph_b64_node_id(b64_node_id: str, tenant: str):
    url = decode_base64urlencoded(b64_node_id)
    # nodes
    result = get_graph(url=url, tenant=tenant)
    result['type_data'] = {}
    # TODO: type specific, move that part
    for n in result['nodes']:
        # find type information
        type_data = get_type_data_from_node_url(n, tenant=tenant)
        result['type_data'][n] = type_data['type_data'].dict()   # TODO: Do we need to encode the URL key?

    return result

@router.get('/{tenant}/config')
def get_config(tenant: str) -> ConfigPost:
    """
    Return default data of if avaliable in db, the one for the tenant
    https://vuetifyjs.com/en/features/theme/#customizing
    """
    dbname = get_db_name_multitenancy()
    with shelve.open(dbname, 'r') as db:
        if tenant in db:
            item = db[tenant]
            return item

    # default
    return ConfigPost()

@router.get('//config')
def get_default_config() -> ConfigPost:
    """
    Default config for the time before the tenant is created
    """
    # default
    return ConfigPost()

@router.post('/{tenant}/config')
def post_config(tenant: str, config: ConfigPost = Body(...)):
    """
    set tenant config data, mainly color and org name
    currently only primary color can be changed
    """
    dbname = get_db_name_multitenancy()
    with shelve.open(dbname) as db:
        db[tenant] = config
