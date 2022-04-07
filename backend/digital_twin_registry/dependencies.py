# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel

class MyBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True