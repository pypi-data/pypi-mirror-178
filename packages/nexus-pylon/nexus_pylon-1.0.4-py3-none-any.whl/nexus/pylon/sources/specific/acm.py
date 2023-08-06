from typing import (
    AsyncIterable,
    Callable,
)

from library.logging import error_log
from nexus.pylon.proxy_manager import AnyOf
from nexus.pylon.sources.base import (
    DoiSeleniumSource,
    PreparedRequest,
)


class AcmSource(DoiSeleniumSource):
    base_url = 'https://dl.acm.org'
    resolve_timeout = 10
    use_proxy = True
    proxy_tags = AnyOf({
        'cambridge',
    })

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        url = f'{self.base_url}/doi/pdf/{self.doi}?download=true'
        yield PreparedRequest(method='get', url=url, timeout=self.timeout)

