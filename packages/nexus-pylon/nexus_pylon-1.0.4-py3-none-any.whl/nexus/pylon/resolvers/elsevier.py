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


class ElsevierResolver(DoiSeleniumSource):
    def get_id_from_resource(self, body):
        if url := body.get('resource', {}).get('primary', {}).get('URL'):
            split = url.split('/')
            if split:
                return split[-1]

    def get_id_from_alternative_id(self, body):
        if aid := body.get('alternative-id'):
            return aid[0]

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        body = await self.resolve_through_doi_org()
        if aid := self.get_id_from_alternative_id(body) or self.get_id_from_resource(body):
            url = f'{self.base_url}/science/article/pii/{aid}/pdfft?isDTMRedir=true&download=true'
            yield PreparedRequest(
                method='get',
                url=url,
                timeout=self.timeout,
            )
