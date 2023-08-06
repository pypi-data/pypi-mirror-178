import re
from typing import AsyncIterable, Optional, List

from library.logging import error_log
from nexus.pylon.exceptions import RegexNotFoundError
from nexus.pylon.proxy_manager import ProxyManager
from nexus.pylon.resolvers.base import BaseResolver

from nexus.pylon.sources.base import PreparedRequest


class LibgenDoiResolver(BaseResolver):
    def __init__(
        self,
        doi,
        proxy_tags: Optional[List] = None,
        proxy_manager: Optional[ProxyManager] = None,
    ):
        super().__init__(proxy_tags=proxy_tags, proxy_manager=proxy_manager)
        self.doi = doi

    async def resolve(self) -> AsyncIterable[PreparedRequest]:
        async with self.get_session() as session:
            url = f'http://libgen.rocks/ads.php?doi={self.doi}'
            async with PreparedRequest(
                method='get',
                url=url,
                timeout=10.0,
            ).execute_with(session=session) as resp:
                downloaded_page_bytes = await resp.read()
                downloaded_page = downloaded_page_bytes.decode('utf-8', 'backslashreplace')
            match = re.search(
                r'(https?:\/\/.*\/)*get\.php\?md5=[a-fA-F\d]+&key=[A-Za-z\d]+(&doi=[^\"]*)+',
                downloaded_page,
                re.IGNORECASE,
            )
            if match:
                if match.group(1):
                    yield PreparedRequest(method='get', url=match.group(0), timeout=10.0)
                else:
                    yield PreparedRequest(method='get', url=f'http://libgen.rocks/{match.group(0)}', timeout=10.0)
            else:
                error_log(RegexNotFoundError(url=url, downloaded_page=downloaded_page[:100]))
