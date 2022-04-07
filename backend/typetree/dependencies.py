# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import os
import shelve
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    acapy_api: str = ''
    dt_twin_registry: str = ''
    acapy_webhook_base_url: str = ''
    organization_name: str = 'Organization Name'
    primary_color: str = '#1976D2'

    class Config:
        env_file = '.env'

@lru_cache()
def get_settings():
    ENV_FILE = os.getenv('ENV_FILE', '.env')
    return Settings(_env_file=ENV_FILE)

settings: Settings = get_settings()


ITEMTYPE_TYPE = os.getenv('ITEMTYPE_TYPE', 'http://supplytree.org/ns/ItemType')
CO2_TYPE = os.getenv('CO2_TYPE', 'http://supplytree.org/ns/CO2')
DB_NAME = os.getenv("DB_NAME", "database.db")
DB_NAME_REMOTE_TYPES = os.getenv("DB_NAME_REMOTE_TYPES", "database_remote_types.db")
DB_NAME_UUID_HEAD = os.getenv('DB_NAME_UUID_HEAD', "uuid_heads.db")
# DB_TYPE_NAME_HEAD = os.getenv('DB_TYPE_NAME_HEAD', "db_type_name_head.db")
SUPPLYTREE_API = os.getenv("SUPLYTREE_API", "http://localhost:3000")

TYPETREE_BASE_URL = os.getenv('TYPETREE_BASE_URL', "http://localhost:8000")
DT_TWIN_REGISTRY = settings.dt_twin_registry

ACAPY_API = settings.acapy_api

ORGANIZATION_NAME = settings.organization_name

class SchemaConfig:
  allow_population_by_field_name = True


def get_acapy_access_token(tenant: str):
    dbname = get_db_name_ssi(tenant=tenant)
    with shelve.open(dbname, 'r') as db:
        token = db['wallet_token']
        return token
    return ''

def get_db_name_base(tenant: str) -> str:
    return 'base_' + tenant + '.db'

def get_db_name_remote_types(tenant: str) -> str:
    return 'remote_types_' + tenant + '.db'

def get_db_name_uuid_heads(tenant: str) -> str:
    return 'uuid_heads_' + tenant + '.db'

def get_db_name_ssi(tenant: str) -> str:
    return 'ssi_' + tenant + '.db'

def get_db_name_multitenancy() -> str:
    return 'multitenancy.db'

def get_typetree_base_url(tenant: str) -> str:
    return TYPETREE_BASE_URL + '/' + tenant

def get_webhook_base_url(tenant: str) -> str:
    return settings.acapy_webhook_base_url + '/' + tenant
