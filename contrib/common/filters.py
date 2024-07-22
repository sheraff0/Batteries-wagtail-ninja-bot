from django.db.models import Q


class FilterSetBase:
    filter_set = list()
    exclude_none = True

    def __init__(self, request):
        self.params = request.GET
        self.make()

    @property
    def filters(self):
        return self._filters

    def make(self):
        self._filters = []
        for attr, func in self.filter_set:
            _value = self.params.get(attr)
            if (_value is not None) or not self.exclude_none:
                _method = getattr(self, f"filter_{attr}", None)
                if _method:
                    _filter = _method(_value)
                else:
                    _filter = Q(**{attr: func(_value)})
                self._filters.append(_filter)


class FiltersMixinBase:
    filter_set_class = FilterSetBase

    def get_filters(self, request):
        return self.filter_set_class(request).filters
