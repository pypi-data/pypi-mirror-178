import logging
import re

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


class BmjSource(DoiSeleniumSource):
    base_url = 'https://www.bmj.com'

    def get(self, chrome, url):
        chrome.get(url)
        try:
            WebDriverWait(chrome, 30).until(EC.presence_of_element_located((By.LINK_TEXT, "PDF")))
        except:
            return False
        doi_suffix = self.doi.split('/')[1]
        logging.getLogger('debug').debug({
            'action': 'search',
            'regex': fr'/content/\d+/{doi_suffix}\.full\.pdf'
        })
        if match := re.search(fr'/content/\d+/{doi_suffix}\.full\.pdf', chrome.page_source):
            url = match.group(0)
            logging.getLogger('debug').debug({
                'action': 'matched',
                'url': url
            })
            chrome.get(f'{self.base_url}{url}')
            return True

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        yield PreparedRequest(method='get', url=f'https://doi.org/{self.doi}', timeout=self.timeout)
