from wagtail import hooks

CUSTOM_ICONS = [
    "icons/handshake-o.svg",
    "icons/money-check-dollar-pen.svg",
    "icons/barcode-reader.svg",
    "icons/file-invoice.svg",
    "icons/invoice-solid.svg",
    "icons/car-battery.svg",
    "icons/cost-estimate-solid.svg",
    "icons/coins-fill.svg",
    "icons/histogram.svg",
    "icons/microsoft-excel.svg",
    "icons/md-pricetags.svg",
    "icons/truck-fast.svg",
    "icons/truck-fast.svg",
    "icons/money-calculator-24-filled.svg",
]


@hooks.register("register_icons")
def icons(icons):
    return icons + CUSTOM_ICONS