from apps.catalog.models import Sections

from .common import ReportSqlBase


SELECT = "SELECT product_id"
GROUP_BY = "GROUP BY product_id"
WITH = {
    "sales": f"""
        {SELECT},
            SUM(quantity * (cp.section <> {Sections.SERVICE})::int)::int quantity
        FROM sales_sale ss
        JOIN catalog_product cp ON cp.page_ptr_id=ss.product_id
        {GROUP_BY}""",
    "supplies": f"""
        {SELECT},
            SUM(quantity)::int quantity
        FROM stock_invoiceitem sii
        {GROUP_BY}""",
    "catalog_page": f"""
        SELECT path
        FROM catalog_catalog cc
        JOIN wagtailcore_page wp ON wp.id=cc.page_ptr_id
        LIMIT 1
    """,
}

LEFT_JOIN = lambda source: f"""
LEFT JOIN {source} ON {source}.product_id=wp.id
"""


class PriceList(ReportSqlBase):
    @property
    def sql_statement(self):
        return f"""
WITH sales AS ({WITH["sales"]}),
    supplies AS ({WITH["supplies"]}),
    catalog_page AS ({WITH["catalog_page"]})
SELECT
    wp.id,
    wp.title,
    djct.model,
    LENGTH(wp.path) / 4 - 3 level,
    cp.price,
    COALESCE(supplies.quantity, 0) - COALESCE(sales.quantity, 0) quantity,
    COALESCE(sales.quantity, 0) sold
FROM wagtailcore_page wp
JOIN django_content_type djct ON djct.id=wp.content_type_id
LEFT JOIN catalog_product cp ON cp.page_ptr_id=wp.id
{LEFT_JOIN("sales")}
{LEFT_JOIN("supplies")}
CROSS JOIN catalog_page
WHERE wp.path LIKE catalog_page.path || '%'
ORDER BY wp.path
;
"""
