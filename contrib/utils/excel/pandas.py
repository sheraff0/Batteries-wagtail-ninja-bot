from io import BytesIO
import pandas as pd
import numpy as np

from contrib.utils.patterns.pipeline import AbstractPipeline


class XlsxReader(AbstractPipeline):
    def process(self):
        _df = (pd
            .read_excel(self._source)
            .replace(np.nan, None)
        )
        return _df.to_dict("records")


class XlsxWriter(AbstractPipeline):
    def process(self):
        _df = pd.DataFrame(self._source)
        _buffer = BytesIO()
        with pd.ExcelWriter(_buffer) as writer:
            _df.to_excel(writer, index=False)
        _buffer.seek(0)
        return _buffer
