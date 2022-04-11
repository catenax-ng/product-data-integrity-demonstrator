# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import json
import shelve
import sys, inspect
from abc import ABC, abstractmethod, abstractproperty
import requests
from .dependencies import ACAPY_API
from .ssi_helpers import prepare_headers, send_nonce_credential
from .ssi_templates import NONCE_PRESENTATION_REQUEST

class State:
    pass

class State(ABC):
    NAME = ''
    def __init__(self, connection_id: str, data: dict = {}) -> None:
        super().__init__()
        self.connection_id = connection_id
        self.data = data
    @abstractmethod
    def next(self) -> State:
        """
        Must return None if it can not transition to the next state.
        It must return the next State if it can transition to the
        next state.
        """
        ...
    def __repr__(self) -> str:
        return self.NAME

class StateStart(State):
    NAME = 'start'
    def __init__(self, connection_id: str, data: dict = {}) -> None:
        super().__init__(connection_id, data=data)
    def next(self) -> State:
        print(self.NAME + '->next')
        return StateActive(self.connection_id)

class StateActive(State):
    """
    State transition from an 'active' -> DidVcSent

    If the state of the connection is in ['active'] transition to the next state
    """
    NAME = 'active'
    def __init__(self, connection_id: str, data: dict = {}) -> None:
        super().__init__(connection_id, data=data)
    def next(self) -> State:
        print(self.NAME + '->next')
        # check if connection is active
        r = requests.get(ACAPY_API + '/connections/' + self.connection_id, headers=prepare_headers(tenant=self.data['tenant']))
        if r.status_code == 200:
            j = r.json()
            if j['state'] in ['active']:
                return StateConnectionDidVcSent(self.connection_id, data=self.data)
        return None

class StateConnectionDidVcSent(State):
    """
    Send a nonce VC and if done, transition to the next state.
    """
    NAME = 'didVcSent'
    NONCE_SENT_ID_KEY = 'nonce_sent_cred_ex_id'
    def __init__(self, connection_id: str, data: dict = {}) -> None:
        super().__init__(connection_id, data=data)
    def next(self) -> State:
        print(self.NAME + '->next')
        if not self.NONCE_SENT_ID_KEY in self.data:
            # send
            result = send_nonce_credential(self.connection_id, tenant=self.data['tenant'])
            if result:
                if 'cred_ex_id' in result:
                    self.data[StateConnectionDidVcSent.NONCE_SENT_ID_KEY] = result['cred_ex_id']
        if self.NONCE_SENT_ID_KEY in self.data:
            # move on
            return StateConnectionDidPresentationRequestSent(connection_id=self.connection_id, data=self.data)
        return None

class StateConnectionDidPresentationRequestSent(State):
    """
    Check for the presentation request id and based on the result,
    send a presentation request or move on to the next state
    """
    NAME = 'didPresReqSent'
    PRESENTATION_REQUEST_ID_KEY = 'presentation_request_id'
    PRESENTATION_REQUEST_THREAD_ID_KEY = 'presentation_request_thread_id'
    def __init__(self, connection_id: str, data: dict = {}) -> None:
        super().__init__(connection_id, data=data)
    def next(self) -> State:
        print(self.NAME + '->next')
        if not self.PRESENTATION_REQUEST_ID_KEY in self.data:
            # send
            input = json.loads(NONCE_PRESENTATION_REQUEST)
            input['connection_id'] = self.connection_id
            # DO NOT include the nonce in the request - it's the whole idea that the other end needs to know
            # and MUST NOT see this from the request
            r = requests.post(ACAPY_API + '/present-proof-2.0/send-request', json=input, headers=prepare_headers(tenant=self.data['tenant']))
            if r.status_code == 200:
                j = r.json()
                if 'pres_ex_id' in j:
                    self.data[self.PRESENTATION_REQUEST_ID_KEY] = j['pres_ex_id']
                    self.data[self.PRESENTATION_REQUEST_THREAD_ID_KEY] = j['thread_id']

        if self.PRESENTATION_REQUEST_ID_KEY in self.data:
            # move on
            return StateConnectionDidPresentationRequestReceived(connection_id=self.connection_id, data=self.data)
        return None

class StateConnectionDidPresentationRequestReceived(State):
    NAME = 'didPresReceived'
    PRESENTATION_RECEIVED_ID = 'presentation_received'
    def __init__(self, connection_id: str, data: dict = {}) -> None:
        super().__init__(connection_id, data=data)
    def next(self) -> State:
        print(self.NAME + '->next')
        req_id = ''
        if StateConnectionDidPresentationRequestSent.PRESENTATION_REQUEST_ID_KEY in self.data:
            req_id = self.data[StateConnectionDidPresentationRequestSent.PRESENTATION_REQUEST_ID_KEY]
        
        if req_id and StateConnectionDidPresentationRequestSent.PRESENTATION_REQUEST_THREAD_ID_KEY:
            params = {}
            params['role'] = 'verifier'
            params['state'] = 'presentation-received'
            params['thread_id'] = self.data[StateConnectionDidPresentationRequestSent.PRESENTATION_REQUEST_THREAD_ID_KEY]
            r = requests.get(ACAPY_API + '/present-proof-2.0/records', params=params, headers=prepare_headers(tenant=self.data['tenant']))
            if r.status_code == 200:
                j = r.json()
                if len(j['results']) == 1:
                    self.data[self.PRESENTATION_RECEIVED_ID] = j['results'][0]['pres_ex_id']

        if self.PRESENTATION_RECEIVED_ID in self.data:
            # move on
            return StateConnectionDidVerified(self.connection_id, data=self.data)
        return None

class StateConnectionDidVerified(State):
    NAME = 'didVerified'
    def __init__(self, connection_id: str, data: dict = {}) -> None:
        super().__init__(connection_id, data=data)
    def next(self) -> State:
        print(self.NAME + ': ->next')
        if StateConnectionDidPresentationRequestReceived.PRESENTATION_RECEIVED_ID in self.data:
            id = self.data[StateConnectionDidPresentationRequestReceived.PRESENTATION_RECEIVED_ID]
            r = requests.get(ACAPY_API + '/present-proof-2.0/records/' + id, headers=prepare_headers(tenant=self.data['tenant']))
            if r.status_code == 200:
                j = r.json()
                record = j['results'][0]
                verified = record['verified']
                if verified: # TODO, SECURITY: also check nonce!
                    return StateConnectionFinal(connection_id=self.connection_id, data=self.data)

        return None

class StateConnectionFinal(State):
    NAME = 'finalState'
    def __init__(self, connection_id: str, data: dict = {}) -> None:
        super().__init__(connection_id, data=data)
    def next(self) -> State:
        print(self.NAME + ': FINAL STATE REACHED')

class Storage(ABC):
    """
    Generic / abstract Storage Interface
    """
    @abstractmethod
    def put(self,connection_id:str, data:dict):
        """put / save to the stoarage layer"""
        ...
    @abstractmethod
    def get(self, connection_id:str) -> dict:
        """get some data from the storage layer"""
        ...

class ShelveStorage(Storage):
    """
    Implements state storage with python 'shelve'
    """
    def __init__(self, db_file_path:str = 'ssi_state_storage.db') -> None:
        super().__init__()
        self.db_file_path = db_file_path

    def put(self, connection_id: str, data: dict):
        with shelve.open(self.db_file_path) as db:
            db[connection_id] = data

    def get(self, connection_id:str) -> dict:
        with shelve.open(self.db_file_path, 'r') as db:
            if not connection_id in db:
                return {}
            data = db[connection_id]
            return data


class StateFactory():
    """
    Factory to create an instance of a class of this
    module by the given NAME field of it.
    """
    @staticmethod
    def from_storage(connection_id:str, storage:Storage = ShelveStorage):
        """
        Uses the ShelveStorage as default
        Loads the connection state from the storage
        """
        state_name = 'start'
        data = {}
        try:
            data = storage.get(connection_id=connection_id)
            state_name = data['state']
        except:
            print('could not find data for connection_id: ' + connection_id)
        return StateFactory.from_state_name(state_name=state_name, connection_id=connection_id, data=data)


    @staticmethod
    def from_state_name(state_name: str, connection_id: str, data:dict = {}) -> State:
        this_module = sys.modules[__name__]
        mod_members = inspect.getmembers(this_module)
        for _, my_class in mod_members:
            my_name = getattr(my_class, 'NAME', '')
            if my_name == state_name:
                return my_class(connection_id=connection_id)

class StateMachine():
    """
    Provides easy way to transition states as far as possible
    """
    def __init__(self, state:State, storage:Storage = None) -> None:
        self.state:State = state
        self.storage:Storage = storage

    @staticmethod
    def from_storage(connection_id:str, storage:Storage = ShelveStorage()):
        """
        Uses the ShelveStorage as default
        Loads the connection state from the storage
        """
        state = StateFactory.from_storage(connection_id=connection_id, storage=storage)
        return StateMachine(state=state, storage=storage)

    def run(self) -> str:
        """
        runs all transitions as far as possible
        returns the state (string) that could be reached
        """
        previous_state = self.state
        while self.state:
            previous_state = self.state
            self.state = self.state.next()
        # save state information
        if self.storage:
            data = self.storage.get(connection_id=previous_state.connection_id)
             # merge the loaded and current data
            updated = {**data, **previous_state.data}
            # last but not least, update the state
            updated['state'] = previous_state.NAME
            self.storage.put(connection_id=previous_state.connection_id, data=updated)
        return previous_state.NAME

if __name__ == '__main__':
    # init via state name
    #s = StateFactory.from_state_name('active', 'XXX')
    # and try to transition to the next state until
    # it fails
    #while s:
    #    s = s.next()

    sm = StateMachine.from_storage('my_conn_id')
    reached_state = sm.run()
    print('reached_state: ' + reached_state)
    d = sm.storage.get('my_conn_id')
    print(d)



