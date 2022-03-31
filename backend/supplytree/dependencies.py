# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import os

REFERNECE_DIRECTORY = os.getenv('REFERNECE_DIRECTORY', './references') # nodes from other orgs, typically explicitly added
CACHE_DIRECTORY = os.getenv('CACHE_DIRECTORY', './cache') # typically data objects fetched from other orgs
NODE_DIRECTORY = os.getenv('NODE_DIRECTORY', './nodes')
NEXT_NODE_DIRECTORY = os.getenv('NEXT_NODE_DIRECTORY', './next_nodes') # holds references to newer / "next" version of the node (under the id/hash of the old one)
DATA_DIRECTORY = os.getenv('DATA_DIRECTORY', './data')
DATA_TMP_DIRECTORY = os.getenv('DATA_TMP_DIRECTORY', './data_tmp') # better on the same disk/partition for a fast file renaming

SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:8000/')


FILE_BLOCK_SIZE = 1024

AUTO_FETCH_REFERENCES = os.getenv('AUTO_FETCH_REFERENCES', True) # automatically fetch node for a URL we received from a 3rd party org

def get_reference_directory(tenant: str) -> str:
    return os.path.join(REFERNECE_DIRECTORY, tenant)

def get_cache_directory(tenant: str) -> str:
    return os.path.join(CACHE_DIRECTORY, tenant)

def get_node_directory(tenant: str) -> str:
    return os.path.join(NODE_DIRECTORY, tenant)

def get_next_node_directory(tenant: str) -> str:
    return os.path.join(NEXT_NODE_DIRECTORY, tenant)

def get_data_directory(tenant: str) -> str:
    return os.path.join(DATA_DIRECTORY, tenant)

def get_data_tmp_directory(tenant: str) -> str:
    return os.path.join(DATA_TMP_DIRECTORY, tenant)

def get_node_public_url(tenant: str) -> str:
    return SERVER_BASE_URL + tenant + '/node/'

def get_data_public_url(tenant: str) -> str:
    return SERVER_BASE_URL + tenant + '/data/'
