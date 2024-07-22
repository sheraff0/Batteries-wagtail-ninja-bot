from io import BytesIO
import gzip

from .patterns.pipeline import AbstractPipeline


class GZipStream(AbstractPipeline):
    def process(self):
        return BytesIO(
            gzip.compress(self._source.encode("utf-8")))
