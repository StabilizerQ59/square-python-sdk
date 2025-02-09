# -*- coding: utf-8 -*-

from cachecontrol import CacheControl
from requests import session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from square.http.http_client import HttpClient
from square.http.http_method_enum import HttpMethodEnum
from square.http.http_response import HttpResponse


class RequestsClient(HttpClient):

    """An implementation of HttpClient that uses Requests as its HTTP Client

    Attributes:
        timeout (int): The default timeout for all API requests.

    """

    def __init__(self,
                 timeout=60,
                 cache=False,
                 max_retries=None,
                 backoff_factor=None,
                 retry_statuses=None,
                 retry_methods=None,
                 verify=True,
                 http_client_instance=None,
                 override_http_client_configuration=False):
        """The constructor.

        Args:
            timeout (float): The default global timeout(seconds).

        """
        if http_client_instance == None:
            self.create_default_http_cient(timeout, cache, max_retries,
                                           backoff_factor, retry_statuses,
                                           retry_methods, verify)
        else:
          if override_http_client_configuration == True:
            http_client_instance.timeout = timeout
            http_client_instance.session.verify = verify
            adapters = http_client_instance.session.adapters
            for adapter in adapters.values():
                adapter.max_retries.total = max_retries
                adapter.max_retries.backoff_factor = backoff_factor
                adapter.max_retries.status_forcelist = retry_statuses
                adapter.max_retries.allowed_methods = retry_methods        

          self.timeout = http_client_instance.timeout
          self.session = http_client_instance.session 

    def create_default_http_cient(self,
                                  timeout=60,
                                  cache=False,
                                  max_retries=None,
                                  backoff_factor=None,
                                  retry_statuses=None,
                                  retry_methods=None,
                                  verify=True):
        self.timeout = timeout
        self.session = session()

        retries = Retry(total=max_retries, backoff_factor=backoff_factor,
                        status_forcelist=retry_statuses, allowed_methods=retry_methods)
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        if cache:
            self.session = CacheControl(self.session)

        self.session.verify = verify

    def execute_as_string(self, request):
        """Execute a given HttpRequest to get a string response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.

        Returns:
            HttpResponse: The response of the HttpRequest.

        """
        response = self.session.request(
            HttpMethodEnum.to_string(request.http_method),
            request.query_url,
            headers=request.headers,
            params=request.query_parameters,
            data=request.parameters,
            files=request.files,
            timeout=self.timeout
        )

        return self.convert_response(response, False, request)

    def execute_as_binary(self, request):
        """Execute a given HttpRequest to get a binary response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.

        Returns:
            HttpResponse: The response of the HttpRequest.

        """

        response = self.session.request(
            HttpMethodEnum.to_string(request.http_method),
            request.query_url,
            headers=request.headers,
            params=request.query_parameters,
            data=request.parameters,
            files=request.files,
            timeout=self.timeout
        )

        return self.convert_response(response, True, request)

    def convert_response(self, response, binary, http_request):
        """Converts the Response object of the HttpClient into an
        HttpResponse object.

        Args:
            response (dynamic): The original response object.
            http_request (HttpRequest): The original HttpRequest object.

        Returns:
            HttpResponse: The converted HttpResponse object.

        """
        if binary:
            return HttpResponse(
                response.status_code,
                response.reason,
                response.headers,
                response.content,
                http_request
            )
        else:
            return HttpResponse(
                response.status_code,
                response.reason,
                response.headers,
                response.text,
                http_request
            )
