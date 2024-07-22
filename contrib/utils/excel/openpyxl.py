from io import BytesIO
from pathlib import Path

import openpyxl

from contrib.utils.patterns.pipeline import AbstractPipeline


class XlsxReader(AbstractPipeline):
    def process(self):
        return openpyxl.load_workbook(self._source)


class XlsxWriter(AbstractPipeline):
    def process(self):
        _buffer = BytesIO()
        self._source.save(_buffer)
        _buffer.seek(0)
        return _buffer


class ExcelRendererBase(AbstractPipeline):
    def __init__(self, data, template: openpyxl.Workbook):
        self._template = template
        super().__init__(data)


class StreamToExcel(AbstractPipeline):
    def __init__(self, data, template_path: Path, Renderer: ExcelRendererBase, before=list()):
        self._data = data
        for Class in before:
            self._data = Class(self._data).output
        self._Renderer = Renderer
        super().__init__(template_path, before=[XlsxReader], after=[XlsxWriter])

    def process(self):
        _template = self._source
        return self._Renderer(self._data, _template).output
