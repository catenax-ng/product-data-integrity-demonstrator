# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
import json
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi import Body
from .supplytreee_helper import calc_hash_from_large_file, calc_hash_from_str, extract_hash_from_url
from .models import NodeResponse, SupplyTreeUrlResponse, Node
from .dependencies import *

router = APIRouter(tags=['SupplyTree Private'])

@router.post('/{tenant}/data/')
async def post_data(tenant: str, content: dict = Body(...)) -> SupplyTreeUrlResponse:
    """
    We expect any json object as the body which will be stored as a data object and
    return the corresponding hash.

    Beware, that formating of the json content might change between API input and
    hash calculation. If you don't want this, use "file upload" API!
    """
    data = json.dumps(content)
    hash = calc_hash_from_str(data)
    fn = os.path.join(get_data_directory(tenant=tenant), hash)
    with open(fn, 'w') as f:
        f.write(data)

    return SupplyTreeUrlResponse(url=get_data_public_url(tenant=tenant) + hash)

@router.post('/{tenant}/node/')
async def post_node(node: Node, tenant: str) -> NodeResponse:
    # TODO: check if all data objects exist
    #data = node.json(indent=4, exclude_unset=True)
    # TODO: investigate / file a but. exclude_unset=True removes the data array content
    # but only if 'previous' exists.
    data = node.json(indent=4)
    hash = calc_hash_from_str(data)
    fn = os.path.join(get_node_directory(tenant=tenant), hash)
    with open(fn, 'w') as f:
        f.write(data)

    node_id = get_node_public_url(tenant=tenant) + hash

    # check if there is a previous version mentioned, if yes, we also need to set the pointers to "next" (this) version of it
    if node.previous:
        previous_node_hash = extract_hash_from_url(node.previous)
        fn_next = os.path.join(get_next_node_directory(tenant=tenant), previous_node_hash)
        old = SupplyTreeUrlResponse(url=node_id)
        with open(fn_next, 'w') as f:
            f.write(old.json(indent=4))

    return NodeResponse(id=node_id, node=node)

@router.post('/{tenant}/data/file_upload')
async def post_data_file_upload(tenant: str, uploaded_file: UploadFile = File(...)):
        """
        Directly stores the uploaded file and calculates the hash that will be returned.
        """
        temp_id = str(uuid.uuid4())
        fn = os.path.join(DATA_TMP_DIRECTORY, temp_id)
        with open(fn, 'wb') as f:
            while block := uploaded_file.file.read(FILE_BLOCK_SIZE):
                f.write(block)
        hash = calc_hash_from_large_file(fn) # yes, this iterates over the file again...
        if not os.path.isfile(fn):
            raise HTTPException(status_code=500, detail="File upload did not work properly. Tmp file name: " + fn)

        fn_final = os.path.join(get_data_directory(tenant=tenant), hash)
        shutil.move(fn, fn_final)
        return SupplyTreeUrlResponse(url=get_data_public_url(tenant=tenant) + hash)
