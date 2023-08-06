from typing import AsyncIterable, List, Optional, Dict

from nexus.pylon.proxy_manager import ProxyManager
from nexus.pylon.resolvers.base import BaseResolver
from nexus.pylon.sources.base import PreparedRequest


def default_link_predicate(link):
    return 'URL' in link


class DoiOrgRequestResolver(BaseResolver):
    def __init__(
        self,
        link_predicate=default_link_predicate,
        timeout: float = 10.0,
        resolve_timeout: float = 10.0,
        proxy_tags: Optional[List] = None,
        proxy_manager: Optional[ProxyManager] = None,
    ):
        super().__init__(proxy_tags=proxy_tags, proxy_manager=proxy_manager)
        self.link_predicate = link_predicate
        self.timeout = timeout
        self.resolve_timeout = resolve_timeout

    async def resolve_through_doi_org(self, params):
        async with self.get_session() as session:
            doi_url = f'https://doi.org/{params["doi"]}'
            async with PreparedRequest(
                method='get',
                url=doi_url,
                timeout=self.resolve_timeout,
                headers={'Accept': 'application/json'}
            ).execute_with(session=session) as resp:
                return await resp.json()

    async def resolve(self, params: Dict) -> AsyncIterable[PreparedRequest]:
        body = await self.resolve_through_doi_org(params)
        if links := body.get('link'):
            for link in links:
                if self.link_predicate(link):
                    yield PreparedRequest(
                        method='get',
                        url=link['URL'],
                        timeout=self.timeout,
                    )
                    return
            yield PreparedRequest(
                method='get',
                url=links[0]['URL'],
                timeout=self.timeout,
            )
