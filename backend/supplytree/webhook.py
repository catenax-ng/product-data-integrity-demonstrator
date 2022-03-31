# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import os
import uuid
import shelve
import requests
from typing import Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pydantic.networks import AnyHttpUrl
from .models import DataNodeBase, Node

router = APIRouter(tags=['Webhook'])

DB_WEBHOOK_SUBSCRIPTION_STATE = os.getenv("DB_WEBHOOK_SUBSCRIPTION_STATE", "webhook_subscription_state.db")

WEBHOOK_SUBSCRIPTION_AUTO_ACK = os.getenv('WEBHOOK_SUBSCRIPTION_AUTO_ACK', True)

STATE_RECEIVED = 'received'
STATE_CONFIRMATION_CODE_SENT = 'confirmation_code_sent'
STATE_CONFIRMATION_CODE_RECEIVED = 'confirmation_code_received'
STATE_ACK_SENT = 'ACK_SENT'

DIRECTION_INCOMING = 'incoming'
DIRECTION_OUTGOING = 'outgoing'

class WebhookSubscribe(BaseModel):
  webhook_endpoint: AnyHttpUrl
  data_type: str

class WebhookSubscribeProcess(BaseModel):
  application_code: str

class WebhookSubscribeConfirm(BaseModel):
  application_code: str
  confirmation_code: str

class WebhookSubscriptionState(BaseModel):
  """ internal storage """
  webhook_endpoint: AnyHttpUrl
  data_type: str
  confirmation_code: str
  direction: Union[DIRECTION_INCOMING, DIRECTION_OUTGOING]
  state: Union[STATE_RECEIVED, STATE_CONFIRMATION_CODE_SENT, STATE_CONFIRMATION_CODE_RECEIVED, STATE_ACK_SENT]




@router.post('/webhook/subscribe')
async def webhook_subscribe(data: Union[WebhookSubscribe, WebhookSubscribeProcess, WebhookSubscribeConfirm]):
  """
  Receiver Webhook endpoint and desired Data Type
  {
    "webhook_endpoint" : "http://.../webhook",
  }

  return: {
    "code" : <e.g. uuid4>
  }
  """
  if isinstance(data, WebhookSubscribe):
    application_code = str(uuid.uuid4())
    state_storage =  WebhookSubscriptionState.parse_obj(data.dict())
    state_storage.direction = DIRECTION_INCOMING
    state_storage.state = STATE_RECEIVED
    with shelve.open(DB_WEBHOOK_SUBSCRIPTION_STATE) as db:
      db[application_code] = state_storage

    confirmation_code = str(uuid.uuid4())
    state_storage.confirmation_code = confirmation_code
    
    r = requests.post(state_storage.webhook_endpoint, WebhookSubscribeConfirm(application_code=application_code, confirmation_code=confirmation_code))
    if r.status_code == 200:
      state_storage.state = STATE_CONFIRMATION_CODE_SENT
      with shelve.open(DB_WEBHOOK_SUBSCRIPTION_STATE) as db:
        db[application_code] = state_storage

@router.get('/webhook/states')
async def webhook_states_private() -> WebhookSubscriptionState:
  """
  TODO: THIS MUST BE A PRIVATE API!!!
  """
  with shelve.open(DB_WEBHOOK_SUBSCRIPTION_STATE) as db:
    all = db.values()
    return all

@router.post('/webhook/subscribe/confirm')
async def webhook_subscribe_confirm():
  """
  {
    "confirmation_code" : "<e.g. uuid4>",
    "reply_to" : "http://.../webhook/confirm/code"
  }
  """
  pass

@router.post('/webhook/subscribe/confirm/code')
async def webhook_subscribe_confirm_code():
  """
  {
    "confirmation_code" : "<e.g. uuid4>",
    "final_ack" : "http://.../webhook/ack"
  }
  """
  pass

@router.post('/webhook/ack')
async def webhook_ack():
  """
  {
    "application_code" : "<e.g. uuid4>"
  }
  """
  pass

@router.post('/webhook')
async def webhook(data: Union[Node, DataNodeBase, WebhookSubscribeConfirm]):
  """
  In the future this might get additional attributes, e.g. whether the sender want to get a signed response or not
  """
  if isinstance(data, WebhookSubscribeConfirm):
    state_storage = None
    with shelve.open(DB_WEBHOOK_SUBSCRIPTION_STATE, 'r') as db:
      state_storage = db[data.application_code]
    
    if not state_storage:
      raise HTTPException(500, "Could not find data for application_code: " + data.application_code)
    
    if not data.confirmation_code == state_storage.confirmation_code:
      raise HTTPException(500, "Confirmation code does not match! Given confirmation_code: " + data.confirmation_code)
    
    state_storage.state = STATE_CONFIRMATION_CODE_RECEIVED
    with shelve.open(DB_WEBHOOK_SUBSCRIPTION_STATE) as db:
      db[data.application_code] = state_storage
    
    return {}





