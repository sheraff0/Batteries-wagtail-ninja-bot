from apps.catalog.models import Sections
from apps.stock.models.scrap import SCRAP_PRICE_DEFAULT
from .common import ReportSqlBase


SELECT = "SELECT product_id"
WHERE = "WHERE {date}"
GROUP_BY = "GROUP BY product_id"
WITH = {
    "sales": f"""
        {SELECT},
            SUM(quantity * (cp.section <> {Sections.SERVICE})::int)::int quantity,
            SUM(ss.price::int * quantity - discount - scrap_value)::int amount,
            SUM(scrap_weight) scrap_weight
        FROM sales_sale ss
        JOIN journal_day jd ON jd.page_ptr_id=ss.day_id
        JOIN catalog_product cp ON cp.page_ptr_id=ss.product_id
        {WHERE}
        {GROUP_BY}
    """,
    "supplies": f"""
        {SELECT},
            SUM(quantity)::int quantity,
            SUM(price::int * quantity)::int amount
        FROM stock_invoiceitem sii
        JOIN stock_invoice si ON si.id=sii.invoice_id
        JOIN journal_day jd ON jd.page_ptr_id=si.day_id
        {WHERE}
        {GROUP_BY}
    """,
    "cogs": f"""
        SELECT sii.product_id,
            sii.price,
            generate_series (1, sii.quantity) count
        FROM stock_invoiceitem sii
        JOIN stock_invoice si ON si.id=sii.invoice_id
        JOIN journal_day jd ON jd.page_ptr_id=si.day_id
        ORDER by jd.date, count, sii.sort_order
    """,
    "catalog_page": f"""
        SELECT path
        FROM catalog_catalog cc
        JOIN wagtailcore_page wp ON wp.id=cc.page_ptr_id
        LIMIT 1
    """,
    "scrap_price": """
        SELECT price scrap_price
        FROM stock_scrapprice
        WHERE date_from <= '{date}'::date
        ORDER BY date_from DESC
        LIMIT 1
    """
}
LEFT_JOIN = lambda source: f"""
LEFT JOIN {source} ON {source}.product_id=cp.page_ptr_id
"""

JOIN_LATERAL_COGS = """LEFT JOIN LATERAL (
    SELECT SUM(price)::int cogs FROM(
        SELECT price
        FROM cogs
        WHERE cogs.product_id=totals.id
        LIMIT sales_quantity OFFSET sales_quantity_start  -- FIFO
    ) subq
) ON true
"""

JOIN_LATERAL_COGS_CUMULATIVE = """LEFT JOIN LATERAL (
    SELECT SUM(price)::int cogs_cumulative FROM(
        SELECT price
        FROM cogs
        WHERE cogs.product_id=totals.id
        LIMIT sales_quantity_end  -- FIFO
    ) subq
) ON true
"""

CALCULATED = [
    "quantity_start", "quantity_end",
    "supplies_amount", "supplies_quantity", "supplies_amount_end",
    "sales_amount", "sales_quantity",
    "sales_scrap_weight", "cogs", "cogs_cumulative"
]
SUMS = ", ".join(f"SUM({x}) {x}" for x in CALCULATED)
JOIN_LATERAL_SUMS = f"""JOIN LATERAL (
    SELECT {SUMS}
    FROM totals t
    WHERE t.path LIKE wp.path || '%'
) ON true
"""


class ProductsReport(ReportSqlBase):
    @property
    def sql_statement(self):
        TOTALS_BY_PRODUCT = f"""
WITH
    sales_0 AS ({WITH["sales"].format(date=self.before_start)}),
    sales_1 AS ({WITH["sales"].format(date=self.before_end)}),
    supplies_0 AS ({WITH["supplies"].format(date=self.before_start)}),
    supplies_1 AS ({WITH["supplies"].format(date=self.before_end)})
SELECT
    wp.id,
    wp.path,
    COALESCE(sales_0.quantity, 0) sales_quantity_start,
    COALESCE(sales_1.quantity, 0) sales_quantity_end,
    COALESCE(supplies_1.amount, 0) supplies_amount_end,
    COALESCE(supplies_0.quantity, 0) - COALESCE(sales_0.quantity, 0) quantity_start,
    COALESCE(supplies_1.quantity, 0) - COALESCE(sales_1.quantity, 0) quantity_end,
    COALESCE(supplies_1.quantity, 0) - COALESCE(supplies_0.quantity, 0) supplies_quantity,
    COALESCE(supplies_1.amount, 0) - COALESCE(supplies_0.amount, 0) supplies_amount,
    COALESCE(sales_1.quantity, 0) - COALESCE(sales_0.quantity, 0) sales_quantity,
    COALESCE(sales_1.amount, 0) - COALESCE(sales_0.amount, 0) sales_amount,
    COALESCE(sales_1.scrap_weight, 0) - COALESCE(sales_0.scrap_weight, 0) sales_scrap_weight
FROM catalog_product cp
JOIN wagtailcore_page wp ON wp.id=cp.page_ptr_id
{LEFT_JOIN("sales_0")}
{LEFT_JOIN("sales_1")}
{LEFT_JOIN("supplies_0")}
{LEFT_JOIN("supplies_1")}
"""
        TOTALS_WITH_COGS = f"""
WITH
    totals AS ({TOTALS_BY_PRODUCT}),
    cogs AS ({WITH["cogs"].format(date=self.before_end)})
SELECT
    totals.*,
    COALESCE(cogs, 0) cogs,
    COALESCE(cogs_cumulative, 0) cogs_cumulative
FROM totals
{JOIN_LATERAL_COGS}
{JOIN_LATERAL_COGS_CUMULATIVE}
"""
        TOTALS_TREE = f"""
WITH totals AS ({TOTALS_WITH_COGS}),
    catalog_page AS ({WITH["catalog_page"]})
SELECT
    wp.id,
    wp.title,
    djct.model,
    LENGTH(wp.path) / 4 - 3 level,
    {", ".join(CALCULATED)}
FROM wagtailcore_page wp
JOIN django_content_type djct ON djct.id=wp.content_type_id
{JOIN_LATERAL_SUMS}
CROSS JOIN catalog_page
WHERE wp.path LIKE catalog_page.path || '%'
ORDER BY wp.path
"""
        TOTALS_WITH_MARGINS = f"""
WITH
    totals AS ({TOTALS_TREE}),
    scrap_price AS ({WITH["scrap_price"].format(date=self.end or "2100-01-01")})
SELECT totals.*,
    sales_amount - cogs margin,
    cogs,
    CASE
        WHEN sales_amount > 0
        THEN (100.0 * (sales_amount - cogs) / sales_amount)::int
    END margin_percent,
    CASE
        WHEN sales_amount > 0
        THEN (100.0 * (sales_amount - cogs + sales_scrap_weight * COALESCE(
            scrap_price, {SCRAP_PRICE_DEFAULT}
        )) / sales_amount)::int
    END margin_with_scrap,
    supplies_amount_end - cogs_cumulative amount_end
FROM totals
CROSS JOIN scrap_price
;
"""
        return TOTALS_WITH_MARGINS
