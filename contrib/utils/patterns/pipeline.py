import abc


class AbstractPipeline(abc.ABC):
    def __init__(self,
        source,
        before: list = list(),
        after: list = list()
    ):
        self._source = source
        self._before = before
        self._after = after
        self.full_process()

    @abc.abstractmethod
    def process(self):
        return self._source

    def before(self):
        for Class in self._before:
            self._source = Class(self._source).output

    def after(self):
        for Class in self._after:
            self._output = Class(self._output).output

    def full_process(self):
        self.before()
        self._output = self.process()
        self.after()

    @property
    def output(self):
        return self._output

