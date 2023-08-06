from typing import (
    AsyncIterable,
    Callable,
)

from library.logging import error_log
from nexus.pylon.sources.base import (
    DoiSeleniumSource,
    PreparedRequest,
)


class ScienceSource(DoiSeleniumSource):
    base_url = 'https://www.science.org'
    resolve_timeout = 10

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        url = f'{self.base_url}/doi/pdf/{self.doi}?download=true'
        yield PreparedRequest(
            method='get',
            url=url,
            timeout=self.timeout,
        )
