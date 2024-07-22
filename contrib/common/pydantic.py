import json

from pydantic import BaseModel


def json_clean(data: BaseModel):
    return json.loads(data.model_dump_json(exclude_none=True))


def construct_params(
    params: BaseModel,
    replace: dict = dict()
):
    _params = []
    for k, v in json_clean(params).items():
        k = replace.get(k, k)
        if type(v) == list:
            for item in v:
                _params.append((k, item))
        else:
            _params.append((k, v))
    return _params
