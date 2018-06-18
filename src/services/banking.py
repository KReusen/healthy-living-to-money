import json
from os.path import isfile
from typing import Optional
import socket

import requests
from bunq.sdk.client import Pagination
from bunq.sdk.context import ApiContext
from bunq.sdk.context import ApiEnvironmentType
from bunq.sdk.context import BunqContext
from bunq.sdk.exception import BunqException
from bunq.sdk.model.generated import endpoint
from bunq.sdk.model.generated.object_ import Pointer, Amount, NotificationFilter

from managers.parameter import ParameterManager

from models.payment_info import PaymentInfo

class BunqService():
    def __init__(self):
        self.parameter_manager = ParameterManager()
        self._authenticate()

    def _authenticate(self):
        if self.parameter_manager.exists("/bunq/api_context"):
            self.api_context = self._get_api_context_from_aws()
            self._ensure_active_session()
        else:
            self.api_context = self._create_api_context()
        
        BunqContext.load_api_context(self.api_context)

    def _get_api_context_from_aws(self) -> ApiContext:
        json_string = self.parameter_manager.get("/bunq/api_context")
        return ApiContext.from_json(json_string)

    def _create_api_context(self) -> ApiContext:
        api_key = self.parameter_manager.get('/bunq/api_key')
        api_context = ApiContext(
            ApiEnvironmentType.PRODUCTION, 
            api_key,
            'runs-to-gadgetfund'
        )
        self._update_remote_api_context(api_context)
        return api_context
    
    def _ensure_active_session(self):
        if not self.api_context.is_session_active():
            self.api_context.reset_session()
            self._update_remote_api_context(self.api_context)
    
    def _update_remote_api_context(self, api_context: object):
        self.parameter_manager.store("/bunq/api_context", api_context.to_json())

    def make_payment(self, PaymentInfo: object):
        recipient = Pointer('IBAN', PaymentInfo.to_iban, "bunq")
        endpoint.Payment.create(
            amount=Amount(PaymentInfo.amount_string, 'EUR'),
            counterparty_alias=recipient,
            description=PaymentInfo.description,
            monetary_account_id=self._get_monetary_account_id_from_iban(PaymentInfo.from_iban)
        )
    
    def _get_monetary_account_id_from_iban(self, from_iban: str) -> Optional[int]:
        all_accounts = self._get_all_active_monetary_accounts()
        account_ids_by_iban = {}
        for account in all_accounts:
            for alias in account["alias"]:
                if alias["type"] == "IBAN":
                    iban = alias["value"]
                    continue
            account_id = account["id"]
            account_ids_by_iban[iban] = account_id
        
        return account_ids_by_iban.get(from_iban)

    def _get_all_active_monetary_accounts(self):
        pagination = Pagination()
        pagination.count = 100

        all_monetary_account_bank = endpoint.MonetaryAccountBank.list(
            pagination.url_params_count_only).value
        all_monetary_account_bank_active = []

        for monetary_account_bank in all_monetary_account_bank:
            if monetary_account_bank.status == "ACTIVE":
                account_to_append = json.loads(monetary_account_bank.to_json())
                all_monetary_account_bank_active.append(account_to_append)

        return all_monetary_account_bank_active
