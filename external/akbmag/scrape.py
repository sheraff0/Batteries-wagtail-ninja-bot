from copy import deepcopy
import json
from multiprocessing import Pool
import os
from pathlib import Path
import re
import requests
from unidecode import unidecode

from box import Box
from bs4 import BeautifulSoup

from apps.catalog.models.common import Polarity, CaseFormat
from contrib.common.cached import acached
from contrib.utils.date_time import timeit

ROOT_URL = "https://akbmag.ru/akkumulyator-dlya/"
SOURCE_ROOT = Path("external/akbmag/html")

CAR_MODELS_MAP_SOURCE = Path("external/akbmag/scrape.json")
CAR_MODELS_MAP = None
CAR_MODELS_INDEX = []

if CAR_MODELS_MAP_SOURCE.is_file():
    with open(CAR_MODELS_MAP_SOURCE) as f:
        CAR_MODELS_MAP = json.loads(f.read())
        CAR_MODELS_INDEX = [
            {
                "section": section["name"],
                "full_name": " ".join((brand["name"], model["name"])),
                **model
            }
            for section in CAR_MODELS_MAP
            for brand in section["brands"]
            for model in brand["models"]
        ]

CAR_MODELS_LIMIT = 10


class AkbMagGetter:
    def get_page(self, url: str):
        path = url.replace(ROOT_URL, "")
        path_elements = re.findall(r"[^/]+", path)

        if len(path_elements) > 1:
            directory = "/".join(path_elements[:-1])
            filename = path_elements[-1] + ".html"
        else:
            directory = path_elements[-1] if path_elements else ""
            filename = "_index.html"

        source = SOURCE_ROOT / directory / filename
        if source.is_file():
            print(f"{url} - reading from file...")
            with open(source, "rb") as f:
                content = f.read()
        else:
            print(f"{url} - loading...")
            content = self.get(url)

            os.makedirs(SOURCE_ROOT / directory, exist_ok=True)
            with open(source, "wb") as f:
                f.write(content)
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def get(self, url):
        r = requests.get(url)
        return r._content


class AkbMagScraper:
    def __init__(self):
        self._getter = AkbMagGetter()

    def parse_root(self):
        root_page = self._getter.get_page(ROOT_URL)
        sections = root_page.find_all("h2")
        res = [*map(self.parse_section, sections)]
        with open(CAR_MODELS_MAP_SOURCE, "w") as f:
            f.write(json.dumps(res, ensure_ascii=False))

    def parse_section(self, section):
        res = {"name": section.text}
        brands_list = section.find_next("div", {"itemtype": "https://schema.org/ItemList"})
        brands = brands_list and brands_list.find_all("div", {"itemprop": "itemListElement"}) or []
        res["brands"] = [*map(self.parse_brand_simple, brands)]
        #res["brands"] = [x for x in res["brands"] if "Ford" in x["name"]]
        with Pool(8) as pool:
            res["brands"] = pool.map(self.parse_brand_models, res["brands"])
        return res

    def parse_brand_simple(self, brand):
        return {
            "name": brand.find_next("span", {"itemprop": "name"}).text.replace("Аккумуляторы для ", ""),
            "link": brand.find_next("link")["href"]
        }

    def parse_brand_models(self, brand):
        brand_page = self._getter.get_page(brand["link"])
        models = brand_page.find_all("li", {"itemtype": "https://schema.org/Thing"})
        brand["models"] = [*map(self.parse_model, models)]
        return brand

    def parse_model(self, model, section_key: str = "model"):
        res = {
            "name": model.find_next("a").text.strip(),
            "link": model.find_next("meta")["content"]
        }
        model_page = self._getter.get_page(res["link"])

        if section_key in ("generations", "years"):
            if section_key == "generations":
                YEARS_PATTERN =r"(?P<year_min>(19\d{2}|20\d{2})) ?- ?(?P<year_max>(\d{4}|н.в.))"
                search = re.search(YEARS_PATTERN, res["name"], flags=re.DOTALL)

                if search:
                    _min = int(search.group("year_min"))
                    _max = search.group("year_max")
                    _max = None if _max == "н.в." else int(_max)
                    res.update({"year": {"min": _min, "max": _max}})

            elif section_key == "years":
                YEAR_PATTERN = r"(?P<year>(19\d{2}|20\d{2}))"
                search = re.search(YEAR_PATTERN, res["name"], flags=re.DOTALL)

                if search:
                    _min = _max = int(search.group("year"))
                    res.update({"year": {"min": _min, "max": _max}})

        if generations := model_page.find("div", {"class": "new-generations"}):
            items = generations
            section_key = "generations"
        elif engines := model_page.find("div", {"class": "cars_engines"}):
            items = engines
            section_key = "engines"
        elif models := model_page.find("div", {"class": "cars_models"}):
            items = models
            section_key = "years"
        else:
            #res["products"] = self.parse_products(model_page)
            res["battery_params"] = self.parse_battery_params(model_page)
            return res
        
        items = items.find_all("li", {"itemtype": "https://schema.org/Thing"})
        res[section_key] = [self.parse_model(x, section_key=section_key) for x in  items]
        return res

    def parse_battery_params(self, page):
        """Параметры АКБ:
        полярность обратная, ёмкость 185-235Ач, пусковой ток 1100-1500А,
        тип грузовые (клеммы под конус, выступают над верхней крышкой),
        длина 513-518мм, ширина 223-278мм, высота 223-242мм.
        """
        
        PARAMS_PATTERN = ".*".join((
            r"полярность (?P<polarity>прямая и обратная|прямая|обратная)",
            r"ёмкость (?P<capacity_min>\d+)?(-(?P<capacity_max>\d+))?Ач",
            r"пусковой ток (?P<current_min>\d+)?(-(?P<current_max>\d+))?А",
            r"тип (?P<type>\w+)",
            r"длина (?P<length_min>\d+)?(-(?P<length_max>\d+))?мм",
            r"ширина (?P<width_min>\d+)?(-(?P<width_max>\d+))?мм",
            r"высота (?P<height_min>\d+)?(-(?P<height_max>\d+))?мм",
        ))

        def min_max(k):
            _min = search.group(f"{k}_min")
            _max = search.group(f"{k}_max")
            return {
                "min": int(_min or _max),
                "max": int(_max or _min),
            }

        def mapped(x, key: str):
            return {
                "polarity": {
                    "прямая": Polarity.STRAIGHT,
                    "обратная": Polarity.REVERSE,
                }.get(x),
                "type": {
                    "европейский": CaseFormat.EUROPE,
                    "азиатский": CaseFormat.ASIA,
                    "американский": CaseFormat.AMERICA,
                    "грузовые": CaseFormat.TRUCK,
                }.get(x)
            }[key]

        params = page.find("p", {"class": "what_battery_params"})
        if not params:
            return
        params = params and params.text.strip()

        search = re.search(PARAMS_PATTERN, params, flags=re.DOTALL)
        res = {
            **{k: mapped(search.group(k), k) for k in ("polarity", "type")},
            **{k: min_max(k) for k in ("capacity", "current", "length", "width", "height")}
        }
        return res


class AkbMagSearch:
    def __init__(self, q: str):
        self.q = q
        self.extract_year()
        _pattern = ".*".join(re.findall("\w+", self.q))
        self.pattern = "|".join(set((_pattern, unidecode(_pattern))))

    def extract_year(self):
        self.year = re.search(r"\w+\W+(19\d{2}|20\d{2})\W?", self.q)
        if self.year:
            self.year = self.year.group(1)
            self.q = self.q.replace(self.year, "")
            self.year = int(self.year)

    def search(self):
        self.res = []
        for model in CAR_MODELS_INDEX:
            search = re.search(self.pattern, model["full_name"], flags=re.IGNORECASE)
            if search:
                self.select_model(model)
                if len(self.res) >= CAR_MODELS_LIMIT:
                    break
        return self.res

    def select_model(self, model):
        _model = deepcopy(model)
        if ("battery_params" in _model) and not self.year:
            self.res.append(_model)
            return

        _generations = _model.pop("generations", _model.pop("years", None))

        if self.year:
            _generations = [x for x in _generations or []
                if (_year := x.get("year")) and
                (_year.get("min") <= self.year <= (_year.get("max") or 2999))
            ]

        if _generations:
            _model["generations"] = _generations
            self.res.append(_model)

    def __call__(self):
        return self.search()


akbmag_scraper = AkbMagScraper()


@acached(ttl=12*3600)
async def _search_akb(q: str):
    return AkbMagSearch(q)()


@timeit
async def search_akb(q: str):
    return await _search_akb(q.lower())


def get_url_params(battery_params):
    _bp = Box(battery_params)
    return dict(
        section=1,
        **({"case_format": _bp.type} if _bp.type else {}),
        **({"polarity": _bp.polarity} if _bp.polarity else {}),
        capacity__gte=_bp.capacity.min,
        capacity__lte=_bp.capacity.max,
        current__gte=_bp.current.min,
        current__lte=_bp.current.max,
        length__gte=_bp.length.min,
        length__lte=_bp.length.max,
        width__gte=_bp.width.min,
        width__lte=_bp.width.max,
        height__gte=_bp.height.min,
        height__lte=_bp.height.max,
    )
