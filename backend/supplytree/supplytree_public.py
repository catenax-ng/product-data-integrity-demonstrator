# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
import json
import uuid
import requests
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse

from .supplytreee_helper import calc_hash_from_large_file, extract_hash_from_url
from .dependencies import *
from .models import UrlList

ACCEPT_HEADER_JSON='application/json'
ACCEPT_HEADER_FILE='application/octet-stream'
ACCEPT_HEADER_WILDCARD='*/*'

router = APIRouter(tags=['SupplyTree Public'])

@router.get(
    '/{tenant}/data/{hash}',
    responses={
        200: {
            "content": {
                "": {},
                "application/json": {},
                "application/octet-stream": {}
            },
            "description": "If selected media type is not possible (e.g. json), a server error will be returned. If not given, the system will decide.",
        },
    })
async def get_data(hash: str, request: Request, tenant: str):
    """
    Returns data for given hash

    Depending on the "accept" header it returns, e.g. application/json or application/octet-stream or if empty,
    it tries to detect from the data object itself.
    """
    fn = os.path.join(get_data_directory(tenant=tenant), hash)
    if not os.path.isfile(fn):
        raise HTTPException(status_code=404, detail="Data not found")
    # TODO: Find a library for the following... or find out how to easier do this in fastapi
    accept_header = request.headers.get('accept')
    accepts = accept_header.split(',')
    if ACCEPT_HEADER_JSON in accepts:
        # TODO: check size limit, etc
        content = ''
        try:
            with open(fn, 'r') as f:
                content = f.read()
                j = json.loads(content)
                return j
        except:
            raise HTTPException(status_code=500, detail="Requested data object is not json. Please use different accept header.")

    elif ACCEPT_HEADER_FILE in accepts:
        return FileResponse(fn, media_type='application/octet-stream')
    else:
        return FileResponse(fn)

@router.get('/{tenant}/node/{hash}')
async def get_node(hash: str, tenant: str, next_version: bool = False):
    """
    Returns the node object for the given hash.

    If "next" is True, an object with a reference to a possible newer version is returned.
    This is a separate API endpoint '/next/node/{hash}' but it is easier to just append "next" query params to a given URL.
    """
    if next_version:
        return await get_next_node(hash=hash, tenant=tenant)

    fn = os.path.join(get_node_directory(tenant=tenant), hash)
    if not os.path.isfile(fn):
        raise HTTPException(status_code=404, detail="Node object not found")
    return FileResponse(fn, media_type=ACCEPT_HEADER_JSON) # TODO: Also consider other accept headers similar to the /data endpoint

@router.get('/{tenant}/next/node/{hash}')
async def get_next_node(hash: str, tenant: str):
    """
    In case there is a newer ("next") version of the given node object (hash), we return the reference to it.

    If not, 404 (which you should consider as the "default" / most often response here)
    """
    fn = os.path.join(get_next_node_directory(tenant=tenant), hash)
    if not os.path.isfile(fn):
        raise HTTPException(status_code=404, detail="No newer version of this node object is known to the system")
    return FileResponse(fn, media_type=ACCEPT_HEADER_JSON)

@router.post('/{tenant}/references')
async def post_references(urls: UrlList, tenant: str):
  """
  Might be restricted in the future

  Takes a list of urls and fetches (if AUTO_FETCH_REFERENCES is True) the content from those urls.

  The system considers the content fetched as Node objects.

  It checks if the hash of the url and the downloaded content matches.

  If an error occurs, fix and retry the entire list, because there is no indication which part of the list
  was successful and which not.
  """
  if AUTO_FETCH_REFERENCES:
    for url in urls.urls:
      url = str(url)
      hash_given = extract_hash_from_url(url)
      r = requests.get(url, headers={'accept': ACCEPT_HEADER_FILE})
      if not r.status_code == 200:
        raise HTTPException(500, "Could not fetch url: " + url)

      # r.raw.encode = True # let requests encode potential gzip file content

      temp_id = str(uuid.uuid4())
      fn = os.path.join(DATA_TMP_DIRECTORY, temp_id)
      with open(fn, 'wb') as f:
          content = r.content
          f.write(content)
      hash = calc_hash_from_large_file(fn) # yes, this iterates over the file again...
      if not os.path.isfile(fn):
          raise HTTPException(status_code=500, detail="File storage did not work properly. Tmp file name: " + fn)

      if hash != hash_given:
        raise HTTPException(status_code=500, detail="At least 1 hash of the given urls did not match the downloaded content. "
          "URL: {0} hash_from_url: {1} hash_calculated_from_download: {2}".format(url, hash_given, hash))

      fn_final = os.path.join(get_reference_directory(tenant=tenant), hash)
      shutil.move(fn, fn_final)
      return {}



