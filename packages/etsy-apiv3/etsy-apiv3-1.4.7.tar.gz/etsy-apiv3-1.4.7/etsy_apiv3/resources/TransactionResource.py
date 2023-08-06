from dataclasses import dataclass
from ..utils import EtsySession, Response
from ..models import Transaction


@dataclass
class TransactionResource():
    session: EtsySession
    __endpoint = "shops/{shop_id}"
    
    def get_transactions_by_listing_id(self, shop_id: int, listing_id: int, limit=25, offset=0) -> Response[Transaction]:
        url = f"{self.__endpoint.format(shop_id=shop_id)}/listings/{listing_id}/transactions"

        json = self.session.request(url, params={"limit":limit, "offset":offset})
        return Response[Transaction](**json)
    
    def get_transactions_by_receipt_id(self, shop_id: int, receipt_id: int) -> Response[Transaction]:
        url = self.__endpoint.format(shop_id=shop_id) + f"/receipts/{receipt_id}/transactions"
        json = self.session.request(url)
        
        return Response[Transaction](**json)

    def find_one(self, shop_id: int, transaction_id: int) -> Transaction:
        url = self.__endpoint.format(shop_id=shop_id) + f"/transactions/{transaction_id}"
        json = self.session.request(url)
        return Transaction(**json)
    
    def find(self, shop_id: int):
        url = self.__endpoint.format(shop_id=shop_id) + f"/transactions"
        json = self.session.request(url)
        return Response[Transaction](**json)