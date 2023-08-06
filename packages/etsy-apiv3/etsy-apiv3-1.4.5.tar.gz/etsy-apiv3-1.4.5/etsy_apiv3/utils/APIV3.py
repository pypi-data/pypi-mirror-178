from typing import Optional
from requests_oauthlib import OAuth2Session
from async_oauthlib import OAuth2Session as AsyncOAuth2Session
import requests
from .RequestException import EtsyRequestException

class EtsySession:
    
    def __init__(self,
                 client_key: str,
                 client_secret: str,
                 token: dict,
                 refresh_url="https://api.etsy.com/v3/public/oauth/token",
                 headers: Optional[dict] = None
    ):
        self.CLIENT_KEY = client_key
        self.CLIENT_SECRET = client_secret
        self.TOKEN = token
        self.REFRESH_URL = refresh_url
        self.headers = headers or {"x-api-key": self.CLIENT_KEY}
        self.refresh_kwargs = {
            'client_id': self.CLIENT_KEY,
            'client_secret': self.CLIENT_SECRET,
        }
        
        self.__base_endpoint = "https://openapi.etsy.com/v3/application/"

    @staticmethod
    def token_updater(token):
        return token
    
    def get_or_create_sync_session(self) -> OAuth2Session:
        if hasattr(self, "sync_session"):
            return getattr(self, "sync_session")
        session = OAuth2Session(self.CLIENT_KEY, token=self.TOKEN, auto_refresh_kwargs=self.refresh_kwargs, auto_refresh_url=self.REFRESH_URL, token_updater=self.token_updater)
        setattr(self, "sync_session", session)
        return getattr(self, "sync_session")

    @property
    def me(self) -> dict:
        session = self.get_or_create_sync_session()
        return session.get(f"{self.__base_endpoint}/users/me", headers=self.headers).json()

    @staticmethod
    def create_response(response: requests.Response):
        json: dict = response.json()
        
        if "error" in json.keys():
            raise EtsyRequestException(response.status_code, json["error"])
        
        return json
    
    def request(self, endpoint: str, method="GET", *args, **kwargs) -> dict:
        """ 
        Send Request to target endpoint by method
        
        Args:
            endpoint (str): Api Endpoint Url
            method (str, optional): HTTP Methods [GET, POST, PUT, DELETE, UPDATE]. Defaults to "GET".

        Raises:
            EtsyRequestException: EtsyRequestException(status_code, message)

        Returns:
            json: Json From Request Response
        """
        url = f"{self.__base_endpoint}{endpoint}"
        session = self.get_or_create_sync_session()
        req: requests.Response = session.request(method, url, headers=self.headers, *args, **kwargs)
        
        return self.create_response(req)
        
    
    async def async_request(self, session: AsyncOAuth2Session, endpoint: str, method="GET", *args, **kwargs) -> dict:
            url = f"{self.__base_endpoint}{endpoint}"
            req: requests.Response = await session.get(url=url, headers=self.headers, *args, **kwargs)
            print(req.text)
            json: dict = await req.json()
            
            if "error" in json.keys():
                raise EtsyRequestException(req.status_code, json["error"])
        
            return json
            