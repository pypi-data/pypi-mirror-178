import re
from typing import (
    AsyncIterable,
    Callable,
)

from library.logging import error_log
from nexus.pylon.exceptions import RegexNotFoundError

from .base import (
    BaseSource,
    PreparedRequest,
)


class ResearchGateSource(BaseSource):
    base_url = 'https://www.researchgate.net'
    resolve_timeout = 10

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        async with self.get_resolve_session() as session:
            url = f'{self.base_url}/search'
            async with PreparedRequest(
                method='get',
                url=url,
                timeout=self.resolve_timeout,
                params={'q': self.title},
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
                    yield PreparedRequest(method='get', url=match.group(0), timeout=self.timeout)
                else:
                    yield PreparedRequest(method='get', url=f'{self.base_url}/{match.group(0)}', timeout=self.timeout)
            else:
                error_log_func(RegexNotFoundError(url=url, downloaded_page=downloaded_page))


https://www.researchgate.net/search?q=Public%20Opinion%20Formation%20and%20Group%20Identity%3A%20The%20Politics%20of%20National%20Identity%20Salience%20in%20Post-Crimea%20Russia%20