# coding: utf-8

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

import shelve

from typetree.aspects.models.extra_models import TokenModel  # noqa: F401
from typetree.aspects.models.error_response import ErrorResponse
from typetree.aspects.models.part_typization import PartTypization

from typetree.dependencies import DB_NAME_UUID_HEAD
from typetree.typetree_helper import *
from typetree.aspects.models.urn_bamm_com_catena_x010_context import UrnBammComCatenaX010Context

router = APIRouter()


@router.get(
    "/{tenant}/parttypetwin/{twinId}",
    responses={
        200: {"model": PartTypization, "description": "The request was successful."},
        401: {"model": ErrorResponse, "description": "Payload or user input is invalid. See error details in the payload for more."},
        402: {"description": "The requesting user or client is not authenticated."},
        403: {"description": "The requesting user or client is not authorized to access resources for the given tenant."},
        404: {"description": "The requested Twin has not been found."},
    },
    tags=["PartTypizationAspect"],
    response_model=PartTypization,  # must be given, otherwise excludes don't work!
    response_model_exclude_none=True,
    #response_model_exclude_unset=True,
)
async def get_part_typization(
    tenant: str,
    twinId: str = Path(None, description="An example resource Id."),
) -> PartTypization:

    result: PartTypization = None
    with shelve.open(DB_NAME_UUID_HEAD, 'r') as db:
        node_id = db[twinId]
        result = PartTypization.parse_obj(get_type_data_from_node_url(node_id, tenant=tenant)['type_data'])
        result.context = UrnBammComCatenaX010Context.as_planned
    return result
