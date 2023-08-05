import warnings
import requests
from gettext import gettext as _
from urllib.parse import urljoin


from .exceptions import BadRequestException, NotFoundException, ServerErrorException, AuthErrorException


class BaseAuthClient:
    """ Basic client to access (non)authorized REST APIs """
    def __init__(self, base_url, proxies=None):
        """
        :param base_url: Base URL. API endpoint paths will always be relative to this URL
        :param proxies: requests' proxy dict
        :return:
        """
        self.base_url = base_url
        self.proxies = proxies
        self.session = requests.Session()

    def send(self, relative_path, http_method, **requests_args):
        """
        Subclasses must implement this method, that will be used to send API requests with proper auth
        :param relative_path: URL path relative to self.base_url
        :param http_method: HTTP method
        :param requests_args: kargs to be sent to requests
        :return:
        """
        url = urljoin(self.base_url, relative_path)

        return self.session.request(http_method, url, proxies=self.proxies, **requests_args)

    def get_response_data(self, response, parse_json=True):
        """
        Get response data or throw an appropiate exception
        :param response: requests response object
        :param parse_json: if True, response will be parsed as JSON
        :return: response data, either as json or as a regular response.content object
        """
        if response.status_code in (requests.codes.ok, requests.codes.created):
            if parse_json:
                return response.json()
            return response.content
        elif response.status_code == requests.codes.bad_request:
            response_json = response.json()
            raise BadRequestException(response_json.get("error", False) or response_json.get("errors",
                                                                                             _("Bad Request: {text}").format(text=response.text)))
        elif response.status_code == requests.codes.not_found:
            raise NotFoundException(_("Resource not found: {url}").format(url=response.url))
        elif response.status_code == requests.codes.internal_server_error:
            raise ServerErrorException(_("Internal server error"))
        elif response.status_code in (requests.codes.unauthorized, requests.codes.forbidden):
            raise AuthErrorException(_("Access denied"))
        else:
            raise ServerErrorException(_("Unknown error occurred"))


class NoAuthClient(BaseAuthClient):
    """
    This class provides you with simple unauthenticated access to APIs
    """

    def send(self, relative_path, http_method, **requests_args):
        """
        Make a unauthorized request
        :param relative_path: URL path relative to self.base_url
        :param http_method: HTTP method
        :param requests_args: kargs to be sent to requests
        :return: requests' response object
        """
        if http_method != "get":
            warnings.warn(_("You are using methods other than get with no authentication!!!"))

        return super(NoAuthClient, self).send(relative_path, http_method, **requests_args)


class TokenAuthClient(BaseAuthClient):
    """
    This class provides you with authenticated access to APIs using a token-based HTTP Authentication scheme
    The token will be included in the Authorization HTTP header, prefixed by a keyword (default: "Token"), with whitespace separating the two strings
    """
    def __init__(self, token, *args, header_keyword="Token", **kwargs):
        """
        :param Token: Authentication token
        :param header_keywork: Authorization HTTP header prefix
        :return:
        """
        if not self.base_url.startswith('https'):
            warnings.warn(_("You are using unencrypted token authentication!!!"))

        super(TokenAuthClient, self).__init__(*args, **kwargs)

        self.session.headers.update({"authentication": "{keyword} {token}".format(keyword=header_keyword, token=token)})


class BasicAuthClient(BaseAuthClient):
    """
    This class provides you with authenticated access to APIs using a basic HTTP Authentication scheme
    """
    def __init__(self, user_name, password, *args, **kwargs):
        """
        :param user_name: User name for basic authentication
        :param password: Password for basic authentication
        :return:
        """
        super(BasicAuthClient, self).__init__(*args, **kwargs)

        self.session.auth = (user_name, password)
