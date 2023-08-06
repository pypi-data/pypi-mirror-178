from ..options.currency import Currency
from ..helpers.is_alias import is_alias


class TransferPayload:
    def __init__(
        self,
        origin_id: str,
        to: str,
        currency: str,
        amount: float,
        description: str,
        concept: str,
        emails: list = list(),
    ) -> None:
        self.origin_id = origin_id
        self.to = self.__to(to)
        self.currency = currency
        self.amount = amount
        self.description = description
        self.concept = concept
        self.emails = emails

    def __to(self, to: str) -> bool:
        if is_alias(to):
            return {"label": to}
        else:
            return {"cbu": to}

    def to_json(self):
        return self.__dict__
