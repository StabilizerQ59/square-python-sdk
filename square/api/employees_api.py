# -*- coding: utf-8 -*-

"""
square

This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

from square.api_helper import APIHelper
from square.http.api_response import ApiResponse
from square.api.base_api import BaseApi
from square.http.auth.o_auth_2 import OAuth2


class EmployeesApi(BaseApi):

    """A Controller to access Endpoints in the square API."""

    def __init__(self, config, call_back=None):
        super(EmployeesApi, self).__init__(config, call_back)

    def list_employees(self,
                       location_id=None,
                       status=None,
                       limit=None,
                       cursor=None):
        """Does a GET request to /v2/employees.

        Gets a list of `Employee` objects for a business.

        Args:
            location_id (string, optional): Filter employees returned to only
                those that are associated with the specified location.
            status (EmployeeStatus, optional): Specifies the EmployeeStatus to
                filter the employee by.
            limit (int, optional): The number of employees to be returned on
                each page.
            cursor (string, optional): The token required to retrieve the
                specified page of results.

        Returns:
            ListEmployeesResponse: Response from the API. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/v2/employees'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'location_id': location_id,
            'status': status,
            'limit': limit,
            'cursor': cursor
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        OAuth2.apply(self.config, _request)
        _response = self.execute_request(_request)

        decoded = APIHelper.json_deserialize(_response.text)
        if type(decoded) is dict:
            _errors = decoded.get('errors')
        else:
            _errors = None
        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result

    def retrieve_employee(self,
                          id):
        """Does a GET request to /v2/employees/{id}.

        Gets an `Employee` by Square-assigned employee `ID` (UUID)

        Args:
            id (string): UUID for the employee that was requested.

        Returns:
            RetrieveEmployeeResponse: Response from the API. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/v2/employees/{id}'
        _url_path = APIHelper.append_url_with_template_parameters(_url_path, {
            'id': id
        })
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        OAuth2.apply(self.config, _request)
        _response = self.execute_request(_request)

        decoded = APIHelper.json_deserialize(_response.text)
        if type(decoded) is dict:
            _errors = decoded.get('errors')
        else:
            _errors = None
        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result
