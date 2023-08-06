import logging
from typing import (
    AsyncIterable,
    Callable
)

from library.logging import error_log
from nexus.pylon.sources.base import (
    DoiSeleniumSource,
    PreparedRequest,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RsmuSource(DoiSeleniumSource):
    def get(self, chrome, url):
        chrome.get(url)
        try:
            element = WebDriverWait(chrome, 30).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "PDF")))
            element.click()
        except Exception as e:
            logging.getLogger('debug').debug({
                'action': 'error',
                'error': str(e)
            })
            return False

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        yield PreparedRequest(method='get', url=f'https://doi.org/{self.doi}', timeout=self.timeout)
