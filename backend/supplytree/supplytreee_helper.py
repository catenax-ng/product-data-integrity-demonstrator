# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import base64
import os
import hashlib
import json
from urllib.parse import urlparse
from pydantic.types import Json
import requests
from pydantic.networks import AnyHttpUrl
from .models import Node, SupplyTreeUrlResponse
from .dependencies import DATA_DIRECTORY, FILE_BLOCK_SIZE, NEXT_NODE_DIRECTORY, NODE_DIRECTORY, get_data_directory, get_next_node_directory, get_node_directory, get_node_public_url

class HashException(Exception):
    def __init__(self, message, given, calculated):
        super().__init__(message)
        self.given = given
        self.calculated = calculated


def calc_hash(data, client_hash=''):
    """
    data: FileStorage, a flask wrapper around a stream
    data.stream or proxy functions, e.g. data.read() to read from the stream

    if client_hash is given, it causes an exception if it doesn't match our
    calculation
    """
    # be careful with read() if it's used twice, do a seek(0) in between!
    content = data.read()
    hash = hashlib.sha256(content).hexdigest()
    if client_hash != '':
        if client_hash != hash:
            #response = jsonify(error='',
            #client_hash=client_hash, hash=hash)
            raise HashException(
                "Hash mismatch. Your hash calculation does not match server hash.",
                client_hash,
                hash)

    return hash

def calc_hash_from_str(content: str):
    encoded = content.encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()

def calc_hash_from_large_file(fpath: str) -> str:
    """
    Calculates the hash from a given filename.
    Iterates in blocks over the (large) file.
    """
    hasher = hashlib.sha256()
    with open(fpath, 'rb') as f:
        while c:= f.read(FILE_BLOCK_SIZE):
            hasher.update(c)

    return hasher.hexdigest()

def parse_node_from_file(path: str) -> Node:
    return Node.parse_file(path)

class InvalidNode(Exception):
    pass

def parse_node_from_url(url: str, tenant: str) -> Node:
    """
    Try to fetch from local storage or if doesn't exist, fetch via Url and parse into model
    """
    if isinstance(url, AnyHttpUrl):
        url = str(url)
    path_arr = urlparse(url).path.split('/')
    hash = path_arr[-1]
    fn = os.path.join(get_node_directory(tenant=tenant), hash)
    if os.path.isfile(fn):
        return Node.parse_file(fn)
    
    # if not in local storage, try to fetch from remote via the given URL
    data = requests.get(url)
    if data.status_code != 200:
        raise InvalidNode("Node Id: " + url)
    try:
        n = Node.parse_raw(data.content) # TODO: we should check the content before we parse it.
        return n
    except:
        raise InvalidNode("Could not parse Node data. Node ID: " + url)
    return None

def parse_next_from_url(url: str, tenant: str) -> Node:
    """
    Try to fetch from local storage or if doesn't exist, fetch via Url and parse into model
    Returns
    """
    node_public_url = get_node_public_url(tenant=tenant)
    if url.startswith(node_public_url):
        # local server url... check our own nodes
        path_arr = urlparse(url).path.split('/')
        hash = path_arr[-1]
        fn = os.path.join(get_next_node_directory(tenant=tenant), hash)
        if os.path.isfile(fn):
            return SupplyTreeUrlResponse.parse_file(fn)
    else:
        # if remote, we fetch it from there
        data = requests.get(url)
        try:
            n = SupplyTreeUrlResponse.parse_raw(data.content) # TODO: we should check the content before we parse it.
            return n
        except:
            print("could not fetch / parse: " + url)
            pass
    return None

def parse_data_from_url(url: str, tenant: str) -> dict:
    """
    Try to fetch from local storage or if doesn't exist, fetch via Url and parse into json
    
    Assuming the data object is json conent. If not, it will obviously fail.
    """
    if isinstance(url, AnyHttpUrl):
        url = str(url)
    path_arr = urlparse(url).path.split('/')
    hash = path_arr[-1]
    fn = os.path.join(get_data_directory(tenant=tenant), hash)
    if os.path.isfile(fn):
        with open(fn, 'r') as f:
            content = f.read()
            return json.loads(content)
    
    # if not in local storage, try to fetch from remote via the given URL
    data = requests.get(url)
    return data.json()

def get_data_with_type_from_node(node: Node, type_str: str):
  """
  Returns the list of data objects that matches the given type_str
  """
  result = []
  for d in node.data:
    if d.type == type_str:
      result.append(str(d.url))
  
  return result

"""
def get_data_with_type_from_node_id(node_id: str, type_str: str, tenant: str):
    node = parse_node_from_url(node_id, tenant=tenant)
    return get_data_with_type_from_node(node, type_str)
"""

def extract_hash_from_url(url: str) -> str:
  hash = urlparse(url).path.split('/')[-1]
  return hash

def find_latest_version(node_link: str, tenant: str, max_depth=20):
    """
    Recursively check for "next" versions of nodes to get to the latest version / head

    TODO: Walk through the result to check the links in "previous" to match. Only then, data integrity is given!
    """
    versions = []
    next_url = node_link + '?next_version=True'
    r = parse_next_from_url(next_url, tenant=tenant)
    if r and r.url:
        versions.append(str(r.url))
        if max_depth <=0:
            raise Exception("Max depth reached. Not following any deeper links. Increase max_depth if desired.")
        new_versions = find_latest_version(str(r.url), tenant=tenant, max_depth=max_depth-1)
        versions = versions + new_versions

    return versions

def is_remote_node(node_id: str, tenant: str):
    hash = extract_hash_from_url(node_id)
    fn = os.path.join(get_node_directory(tenant=tenant), hash)
    if os.path.isfile(fn):
        return False

    return True

class MaxDepthReachedException(Exception):
  pass

def get_graph(url: str, tenant: str, max_depth=20):
    """
    Returns Graph of nodes with edges
    """
    result = {}
    result['nodes'] = []
    result['edges'] = []

    node = parse_node_from_url(url, tenant=tenant)
    if node:
        result['nodes'].append(url)
    for n in node.nodes:
        # the nodes
        if max_depth <= 0:
            raise MaxDepthReachedException("Max depth reached. Please set value accordingly if desired.")
        deeper_nodes = get_graph(str(n), tenant, max_depth=max_depth-1)
        result['nodes'] = result['nodes'] + deeper_nodes['nodes']
        # the edges
        result['edges'].append({"from": url, "to": str(n)})

    return result


def decode_base64urlencoded(b64_data:str):
    # python padding issues (a minimum of 3 (could be more...) to get the 4 full)
    # Workaround: https://gist.github.com/perrygeo/ee7c65bb1541ff6ac770
    url = base64.urlsafe_b64decode(b64_data + '===')
    dec_url = url.decode()
    return dec_url
