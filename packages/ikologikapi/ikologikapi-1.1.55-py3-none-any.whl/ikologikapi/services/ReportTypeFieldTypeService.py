import json
from types import SimpleNamespace

import requests

from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.IkologikException import IkologikException
from ikologikapi.domain.Search import Search
from ikologikapi.services.AbstractIkologikCustomerService import AbstractIkologikCustomerService


class ReportTypeFieldTypeService(AbstractIkologikCustomerService):

    def __init__(self, jwtHelper: IkologikApiCredentials):
        super().__init__(jwtHelper)

    # CRUD actions

    def get_url(self, customer: str, installation: str, report_type: str) -> str:
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/installation/{installation}/reporttype/{report_type}/fieldtype'

    def get_by_id(self, customer: str, installation: str, report_type: str, id: str) -> object:
        try:
            response = requests.get(
                self.get_url(customer, installation, report_type) + f'/{id}',
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing get_by_id, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_by_id")

    def list(self, customer: str, installation: str, report_type: str) -> list:
        try:
            response = requests.get(
                f'{self.get_url(customer, installation, report_type)}',
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing list, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing list")

    def search(self, customer: str, installation: str, report_type: str, search) -> list:
        try:
            data = json.dumps(search, default=lambda o: o.__dict__)
            response = requests.post(
                f'{self.get_url(customer, installation, report_type)}/search',
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing search, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing search")

    def create(self, customer: str, installation: str, report_type: str, o: object) -> object:
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.post(
                self.get_url(customer, installation, report_type),
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 201:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing create, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing create")

    def update(self, customer: str, installation: str, report_type: str, o: object):
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.put(
                f'{self.get_url(customer, installation, report_type)}/{o.id}',
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing update, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing update")

    def updateAll(self, customer: str, installation: str, report_type: str, o: list):
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.put(
                f'{self.get_url(customer, installation, report_type)}',
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing update, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing update")

    def delete(self, customer: str, installation: str, report_type: str, id: str):
        try:
            response = requests.delete(
                f'{self.get_url(customer, installation, report_type)}/{id}',
                headers=self.get_headers()
            )
            if response.status_code != 204:
                raise IkologikException("Error while performing delete, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing delete")

    def get_by_code(self, customer: str, installation: str, report_type: str, code: str) -> object:
        # Prepare the search
        search = Search()
        search.add_filter("code", "EQ", [code])
        search.add_order("code", "ASC")
        search.set_pagination(0, 1)

        # Query
        result = self.search(customer, installation, report_type, search)
        if result and len(result) == 1:
            return result[0]
        else:
            return None

    def get_by_name(self, customer: str, installation: str, report_type: str, name: str) -> object:
        # Prepare the search
        search = Search()
        search.add_filter("name", "EQ", [name])
        search.add_order("name", "ASC")
        search.set_pagination(0, 1)

        # Query
        result = self.search(customer, installation, report_type, search)
        if result and len(result) == 1:
            return result[0]
        else:
            return None
