import logging
from typing import AsyncIterable, Dict

from aiohttp.client_exceptions import ClientPayloadError

from library.aiokit.aiokit import AioThing
from library.logging import error_log
from nexus.pylon.exceptions import DownloadError
from nexus.pylon.proto.file_pb2 import FileResponse as FileResponsePb


class Source(AioThing):
    def __init__(self, matcher, resolver, driver):
        super().__init__()
        self.matcher = matcher
        self.resolver = resolver
        self.driver = driver

    def __str__(self):
        return f'Source({self.resolver}, {self.driver})'

    def is_match(self, params):
        return self.matcher.is_match(params)

    async def download(self, params: Dict) -> AsyncIterable[FileResponsePb]:
        yield FileResponsePb(status=FileResponsePb.Status.RESOLVING)
        async for prepared_file_request in self.resolver.resolve(params):
            logging.debug({
                'action': 'download',
                'mode': 'pylon',
                'params': params,
                'source': str(self),
                'prepared_file_request': prepared_file_request,
            })
            try:
                async for resp in self.driver.execute_prepared_file_request(prepared_file_request=prepared_file_request):
                    yield resp
                return
            except ClientPayloadError as e:
                error_log(e, level=logging.WARNING)
                continue
            except DownloadError as e:
                error_log(e)
                continue
        raise DownloadError(error='not_found', params=params, resolver=str(self.resolver), driver=str(self.driver))
