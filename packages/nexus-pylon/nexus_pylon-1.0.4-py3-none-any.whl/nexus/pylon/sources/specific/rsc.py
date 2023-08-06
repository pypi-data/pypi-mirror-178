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

class RscSource(DoiSeleniumSource):
    base_url = 'https://pubs.rsc.org'
    resolve_timeout = 10
    use_proxy = True
    proxy_tags = AnyOf({'edinburg'})

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        async with self.get_session() as session:
            url = f'https://doi.org/{self.doi}'
            async with PreparedRequest(
                method='get',
                url=url,
                timeout=self.resolve_timeout,
                headers={'Accept': 'application/json'}
            ).execute_with(session=session) as resp:
                body = await resp.json()
                if link := body.get('link'):
                    if url := link[0].get('URL'):
                        yield PreparedRequest(
                            method='get',
                            url=url,
                            timeout=self.timeout,
                        )
