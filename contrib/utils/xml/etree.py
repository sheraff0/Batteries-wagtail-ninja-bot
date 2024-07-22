import xml.etree.ElementTree as ET

from contrib.utils.patterns.pipeline import AbstractPipeline


class XMLCreator(AbstractPipeline):
    def create_elements(self, parent, obj):
        if obj is None:
            return
        if type(obj) == dict:
            for k, v in obj.items():
                if k.startswith("@"):
                    attr = k[1:]
                    parent.set(attr, v)
                else:
                    subelement = ET.SubElement(parent, k)
                    self.create_elements(subelement, v)
        elif type(obj) == list:
            for v in obj:
                self.create_elements(parent, v)
        else:
            parent.text = str(obj)

    def process(self):
        print(self._source)
        _roots = []
        for k, v in self._source.items():
            _root = ET.Element(k)
            self.create_elements(_root, v)
            ET.indent(_root)
            _root = ET.tostring(_root).decode()
            _roots.append(_root)
        return "\n".join(_roots)
