from pydantic import BaseModel



class CustomProperty(BaseModel):
    key: str
    value: str


class GoodsCategory(BaseModel):
    id: str
    name: str
    number: int | None = None  # sort_order
    parent: str | None = None
    defaultSubject: int = 1
    defaultTax: int = 6  # НДС не облагается
    defaultUnit: str = "ед"
    defaultUnitCode: int = 0  # Штука или Единица
    defaultMarkingType: int | None = None
    customProperties: list[CustomProperty] | None = None
    defaultPaymentMethodType: int = 4  # Полный расчёт


class SlotInfo(BaseModel):
    slotId: int
    isBlocked: bool | None = False
    maxValue: int


class Goods(BaseModel):
    id: str
    group_id: str
    type: str | None = "simple"  # simple|ingredient|complex
    #productionCost: float
    #marginPercent: float
    isWeight: int | None = 0  # 0-Штучный 1-Весовой
    tax: int | None = 6  # НДС не облагается
    unit: str | None = "ед"
    unitCode: int | None = 0  # Штука или Единица
    subject: int| None = 1  # Товар
    isOrderable: bool | None = False  # Возможность закупки товара у населения
    name: str
    slotInfo: SlotInfo | None = None
    sku: str | None = None
    price: float | None = None
    barcodes: list[str] | None = None
    nonTradable: bool | None = False
    customProperties: list[CustomProperty] | None = None
    paymentMethodType: int | None = 4  # Полный расчёт


class BulkUpsert(BaseModel):
    removeObsolete: bool = False
    nonAtomic: bool = True
    payload: list[object]


class ListGoods(BulkUpsert):
    payload: list[Goods]


class ListGoodsCategory(BulkUpsert):
    payload: list[GoodsCategory]
