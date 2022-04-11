
# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel

from supplytree.models import Node
from .dependencies import CO2_TYPE
from .typetree_helper import parse_node_from_url, get_data_with_type_from_node, parse_data_from_url
from .models import Co2Data, MultipleCo2InformationException

def get_co2_data_from_node_url(url: str, tenant: str) -> Co2Data:
    """
    Reads the CO2 data entry from the list. and returns it as Co2Data
    If 0: returns empty obj (default co2 value '')
    if more than 1: MultipleCo2InformationException because it MUST be only 1
    """
    node: Node = parse_node_from_url(url, tenant=tenant)
    urls = get_data_with_type_from_node(node, CO2_TYPE)
    if len(urls) > 1:
        # we only allow exactly 1
        raise MultipleCo2InformationException
    if len(urls) == 1:
        data = parse_data_from_url(str(urls[0]), tenant=tenant)
        co2: Co2Data = Co2Data.parse_obj(data)
        return co2
    
    return Co2Data() # return empty obj
    
class MaxDepthReachedException(Exception):
    pass

def get_co2_graph_list(url: str, tenant: str, max_depth=20):
    """
    Returns Graph of nodes with its according co2 values
    """
    result = {}
    result['nodes'] = []
    result['edges'] = []
    result['co2'] = {}

    node = parse_node_from_url(url, tenant=tenant)
    if node:
        result['nodes'].append(url)
        co2 = get_co2_data_from_node_url(url, tenant=tenant)
        result['co2'][url] = co2
    for n in node.nodes:
        # the nodes
        if max_depth <= 0:
            raise MaxDepthReachedException("Max depth reached. Please set value accordingly if desired.")
        deeper_nodes = get_co2_graph_list(str(n), tenant=tenant, max_depth=max_depth-1)
        result['nodes'] = result['nodes'] + deeper_nodes['nodes']
        # the edges
        result['edges'].append({"from": url, "to": str(n)})
        # co2
        result['co2'].update(deeper_nodes['co2'])

    return result

def get_co2_sum(url: str, tenant: str, max_depth=20):
    graph = get_co2_graph_list(url, tenant=tenant, max_depth=max_depth)
    sum = 0.0
    item:Co2Data
    for item in graph['co2'].values():
        c = float(item.co2)
        sum = sum + c

    return sum


