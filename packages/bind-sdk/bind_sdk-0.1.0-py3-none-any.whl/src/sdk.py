import logging

from .settings import BIND_PASSWORD, BIND_USER, BIND_END_POINT, REDIS_CONNECTION
from .services.bind_service import BindService
from .services.cache_service import CacheService

logger = logging.getLogger(__name__)


class Sdk:
    def login(self, refresh=False) -> str:
        cs = CacheService()
        if REDIS_CONNECTION:
            if not cs.get_credentials() or refresh:
                rta = BindService.login(BIND_USER, BIND_PASSWORD, BIND_END_POINT)
                cs.set_credentials(rta.get("token"), rta.get("expires_in") - 100)
            return cs.get_credentials()
        else:
            return BindService.login(BIND_USER, BIND_PASSWORD, BIND_END_POINT).get(
                "token"
            )

    def is_bancked(self, cuit: int) -> dict:
        return BindService.bancked_cuit(cuit, str(self.login()), BIND_END_POINT)
