from typing import (
    AsyncIterable,
    Callable,
)

from library.logging import error_log
from nexus.pylon.sources.base import (
    DoiSeleniumSource,
    PreparedRequest,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class NatureSource(DoiSeleniumSource):
    def get(self, chrome, url):
        chrome.get(url)
        element = WebDriverWait(chrome, 30).until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            '#entitlement-box-right-column span',
        )))
        if element:
            chrome.execute_script("arguments[0].click();", element)
            return True
        return False

    async def resolve(self, error_log_func: Callable = error_log) -> AsyncIterable[PreparedRequest]:
        yield PreparedRequest(method='get', url=f'https://doi.org/{self.doi}', timeout=self.timeout)
