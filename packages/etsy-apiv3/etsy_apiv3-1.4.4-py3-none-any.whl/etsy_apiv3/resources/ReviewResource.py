from dataclasses import dataclass
#from etsy_apiv3.utils.APIV3 import EtsyAuth
from etsy_apiv3.utils.Response import Response
from etsy_apiv3.models.ReviewModel import Review
from async_oauthlib import OAuth2Session as AsyncOAuth2Session
from etsy_apiv3.utils.APIV3 import EtsySession

@dataclass
class ReviewResource:
    session: EtsySession
    
    def get_reviews_by_listing_id(self, listing_id: int, limit: int = 25, offset: int = 0):
        
        params = {"limit": limit, "offset": offset}
        url = f"listings/{listing_id}/reviews"
        
        response = self.session.request(url, params=params)
        return Response[Review](**response)
    
    def get_reviews_by_shop_id(self, shop_id: int, limit: int = 25, offset: int = 0):
        
        params = {"limit": limit, "offset": offset}
        url = f"shops/{shop_id}/reviews"
        
        response = self.session.request(url, params=params)
        return Response[Review](**response)
    
    async def async_get_reviews_by_shop_id(self, session: AsyncOAuth2Session, shop_id: int, limit: int = 25, offset: int = 0):
        
        params = {"limit": limit, "offset": offset}
        url = f"shops/{shop_id}/reviews"

        response = await self.session.async_request(session=session, endpoint=url, params=params)
        return Response[Review](**response)