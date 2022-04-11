# coding: utf-8

import shelve
from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from typetree.aspects.models.extra_models import TokenModel  # noqa: F401
from typetree.aspects.models.assembly_part_relationship import AssemblyPartRelationship
from typetree.aspects.models.error_response import ErrorResponse
from typetree.aspects.apis.part_typization_api import get_part_typization
from typetree.aspects.models.urn_bamm_com_catenax_traceability011_setof_child_ids_characteristic_child import UrnBammComCatenaxTraceability011SetofChildIdsCharacteristicChild
from typetree.dependencies import get_db_name_uuid_heads
from typetree.models import ItemType
from typetree.typetree_helper import get_type_data_from_node_url
from typetree.aspects.models.urn_bamm_com_catenax_traceability011_usage_characteristic import UrnBammComCatenaxTraceability011UsageCharacteristic


router = APIRouter()


@router.get(
    "/{tenant}/relationship/{twinId}",
    responses={
        200: {"model": AssemblyPartRelationship, "description": "The request was successful."},
        401: {"model": ErrorResponse, "description": "Payload or user input is invalid. See error details in the payload for more."},
        402: {"description": "The requesting user or client is not authenticated."},
        403: {"description": "The requesting user or client is not authorized to access resources for the given tenant."},
        404: {"description": "The requested Twin has not been found."},
    },
    tags=["AssemblyPartRelationshipAspect"],
    response_model=AssemblyPartRelationship,
    response_model_exclude_none=True,
    #response_model_exclude_unset=True, # doesn't return all elments? strange! a bug?
)
async def get_assembly_part_relationship(
    tenant: str,
    twinId: str = Path(None, description="An example resource Id."),
) -> AssemblyPartRelationship:
    result: AssemblyPartRelationship = None
    dbname = get_db_name_uuid_heads(tenant=tenant)
    with shelve.open(dbname, 'r') as db:
        node_id = db[twinId]
        item_type = ItemType.parse_obj(get_type_data_from_node_url(node_id, tenant=tenant)['type_data'])
        result = AssemblyPartRelationship(catena_x_unique_id=item_type.catena_x_unique_id)
        for component in item_type.child_types:
            c = get_type_data_from_node_url(component, tenant=tenant)['type_data']
            result.child_parts.append(UrnBammComCatenaxTraceability011SetofChildIdsCharacteristicChild(
                child_catena_x_id=c.catena_x_unique_id,
                usage=UrnBammComCatenaxTraceability011UsageCharacteristic.as_planned
            ))

    return result
