import re
from typing import (
    AsyncIterable,
    Callable,
)

from library.logging import error_log
from nexus.pylon.exceptions import RegexNotFoundError

from nexus.pylon.sources.base import (
    DoiSource,
    PreparedRequest,
)


class SciHubSource(DoiSource):
    allowed_content_type = {
        'application/octet-stream',
        'application/pdf',
        'application/pdf;charset=utf-8',
    }
    base_url = None
    ssl = False

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        async with self.get_session() as session:
            url = f'{self.base_url}/{self.doi}'
            async with PreparedRequest(
                method='get',
                url=url,
                timeout=self.resolve_timeout,
            ).execute_with(session=session) as resp:
                # Sometimes sci-hub returns file
                if resp.headers.get('Content-Type') == 'application/pdf':
                    yield PreparedRequest(method='get', url=url, timeout=self.timeout)
                downloaded_page_bytes = await resp.read()
                downloaded_page = downloaded_page_bytes.decode('utf-8', 'backslashreplace')
            match = re.search(r"href='(.*)\?download=true'", downloaded_page, re.IGNORECASE)
            if match:
                url = match.group(1)
                url = url.replace(r'\/', '/')
                if 'http' not in url:
                    if url.startswith('//'):
                        url = 'https:' + url
                    elif 'sci-hub' not in url:
                        url = self.base_url.rstrip('/') + '/' + url.lstrip('/')
                    else:
                        url = 'https://' + url
                yield PreparedRequest(method='get', url=str(url), timeout=self.timeout, params={'download': 'true'})
            else:
                error_log_func(RegexNotFoundError(url=url))


class SciHubMksaTopSource(SciHubSource):
    base_url = 'https://sci-hub.mksa.top'


class SciHubSeSource(SciHubSource):
    base_url = 'https://sci-hub.se'
