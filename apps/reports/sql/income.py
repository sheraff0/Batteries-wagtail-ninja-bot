from apps.stock.models.scrap import SCRAP_PRICE_DEFAULT
from .common import ReportSqlBase


YM = "to_char(jd.date, 'YYYY-MM') ym"

WITH = {
    "sales": f"""
        SELECT product_id,
            {YM},
            SUM(quantity) quantity,
            SUM(price::int * quantity - discount - scrap_value)::int amount,
            SUM(scrap_weight) scrap_weight
        FROM sales_sale ss
        JOIN journal_day jd ON jd.page_ptr_id=ss.day_id
        GROUP BY product_id, ym
    """,
    "cogs": f"""
        SELECT product_id,
            sii.price,
            generate_series (1, sii.quantity) count
        FROM stock_invoiceitem sii
        JOIN stock_invoice si ON si.id=sii.invoice_id
        JOIN journal_day jd ON jd.page_ptr_id=si.day_id
        ORDER by jd.date, count, sii.sort_order
    """,
    "costs": f"""
        SELECT
            SUM((amount / months))::int total_costs,
            to_char(jd.date + delta * interval '1 month', 'YYYY-MM') ym
        FROM finance_cost fc
        JOIN journal_day jd ON jd.page_ptr_id=fc.day_id
        JOIN LATERAL (
            SELECT generate_series (0, months - 1) delta
        ) ON true
        GROUP BY ym
    """,
}

JOIN_LATERAL_SALES_BEFORE = """LEFT JOIN LATERAL (
    SELECT SUM(quantity)::int sales_quantity_0
    FROM sales sales_0
    WHERE sales_0.product_id=sales.product_id
        AND sales_0.ym < sales.ym
) ON true 
"""

JOIN_LATERAL_COGS = """LEFT JOIN LATERAL (
    SELECT SUM(price)::int cogs FROM (
        SELECT price
        FROM cogs
        WHERE cogs.product_id=sales.product_id
        LIMIT sales_quantity OFFSET sales_quantity_0
    )
) ON true
"""

JOIN_LATERAL_SCRAP_PRICE = """LEFT JOIN LATERAL (
    SELECT price scrap_price
    FROM stock_scrapprice ssp
    WHERE to_char(ssp.date_from, 'YYYY-MM') <= sales.ym
    ORDER BY ssp.date_from DESC
    LIMIT 1
) ON true
"""


class IncomeReport(ReportSqlBase):
    @property
    def sql_statement(self):
        SALES = f"""
WITH
    sales AS ({WITH["sales"]})
SELECT
    ym,
    product_id,
    COALESCE(quantity, 0) sales_quantity,
    COALESCE(amount, 0) sales_amount,
    COALESCE(scrap_weight, 0) scrap_weight,
    COALESCE(sales_quantity_0, 0) sales_quantity_0
FROM sales
{JOIN_LATERAL_SALES_BEFORE}
"""
        SALES_WITH_COGS = f"""
WITH
    sales AS ({SALES}),
    cogs AS ({WITH["cogs"]})
SELECT
    sales.*,
    cogs
FROM sales
{JOIN_LATERAL_COGS}
"""
        SALES_TOTALS = f"""
WITH
    sales AS ({SALES_WITH_COGS})
SELECT
    sales.ym,
    SUM(sales_amount) sales,
    SUM(cogs) cogs,
    SUM(scrap_weight) scrap_weight
FROM sales
GROUP BY ym
"""
        INCOME_TOTALS = f"""
WITH
    sales AS ({SALES_TOTALS}),
    costs AS ({WITH["costs"]})
SELECT
    sales.ym,
    sales,
    cogs,
    sales - cogs gross_margin,
    COALESCE(scrap_weight, 0) * COALESCE(
        scrap_price, {SCRAP_PRICE_DEFAULT}
    ) scrap,
    COALESCE(total_costs, 0)::int costs
FROM sales
{JOIN_LATERAL_SCRAP_PRICE}
LEFT JOIN costs ON costs.ym=sales.ym
"""
        INCOME_TOTALS_FINAL = f"""
WITH
    sales AS ({INCOME_TOTALS})
SELECT
    ym,
    sales,
    cogs,
    gross_margin,
    scrap,
    gross_margin + scrap gross_margin_with_scrap,
    costs,
    gross_margin + scrap - costs net_income
FROM sales
ORDER BY ym
"""
        return INCOME_TOTALS_FINAL
