# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supplytree.supplytree_private import router as supplytree_private_router
from supplytree.supplytree_public import router as supplytree_public_router
from typetree.typetree_private import router as typetree_private_router
from typetree.aspects.apis.part_typization_api import router as part_typization_router
from typetree.aspects.apis.assembly_part_relationship_api import router as assembly_part_relationship_router
from typetree.typetree_ssi import router as typetree_ssi_router
from typetree.multitenancy import router as multitenancy_router


app = FastAPI()


# TODO: for development, fix in production
origins = [
    "*",
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"])

app.include_router(multitenancy_router)

app.include_router(supplytree_public_router)
app.include_router(supplytree_private_router)
app.include_router(typetree_private_router)

app.include_router(typetree_ssi_router)

app.include_router(part_typization_router)
app.include_router(assembly_part_relationship_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=5, reload=False)

