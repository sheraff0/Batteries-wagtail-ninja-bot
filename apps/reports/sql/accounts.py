from .common import ReportSqlBase

JOIN_LATERAL_ITEMS = """JOIN LATERAL (
    SELECT SUM(price::int * quantity) supply
    FROM stock_invoiceitem sii
    WHERE sii.invoice_id=si.id
) ON true"""

JOIN_LATERAL_PAYMENTS = lambda field, pattern, not_=False: f"""JOIN LATERAL (
    SELECT SUM(amount) {field}
    FROM finance_invoicepayment fip
    JOIN root_account ra ON ra.id=fip.account_id
    WHERE fip.invoice_id=si.id
        AND {"NOT" if not_ else ""} ra.name ~* '{pattern}'
) ON true"""

JOIN_LATERAL_LAST_INVOICE = """JOIN LATERAL (
    SELECT
        MAX(jd.date) last
    FROM stock_invoice si
    JOIN journal_day jd ON jd.page_ptr_id=si.day_id
    WHERE si.partner_id=rp.id
) ON true
"""

WITH = {
    "invoices": f"""
        SELECT
            si.*,
            jd.date day_date,
            supply,
            paid,
            scrap_value scrap,
            advance,
            debt,
            payments
        FROM stock_invoice si
        JOIN journal_day jd ON jd.page_ptr_id=si.day_id
        {JOIN_LATERAL_ITEMS}
        {JOIN_LATERAL_PAYMENTS("paid", "должны", not_=True)}
        {JOIN_LATERAL_PAYMENTS("advance", "нам должны")}
        {JOIN_LATERAL_PAYMENTS("debt", "мы должны")}
        {JOIN_LATERAL_PAYMENTS("payments", "")}
    """,
    "partners": f"""
        SELECT
            id,
            name,
            last
        FROM root_partner rp
        {JOIN_LATERAL_LAST_INVOICE}
    """,
}


class AccountsReport(ReportSqlBase):
    @property
    def sql_statement(self):
        INVOICES = f"""
WITH
    invoices AS ({WITH["invoices"]}),
    partners AS ({WITH["partners"]})
SELECT
    invoices.*,
    partners.name partner,
    last
FROM invoices
JOIN partners ON partners.id=invoices.partner_id
"""
        INVOICES = f"""
WITH invoices AS ({INVOICES})
SELECT
    partner,
    id, day_date, number, payment_date,
    SUM(supply) supply,
    SUM(paid) paid,
    SUM(scrap) scrap,
    SUM(advance) advance,
    SUM(debt) debt,
    SUM(supply) - SUM(scrap) - COALESCE(SUM(payments), 0) balance
FROM invoices
GROUP BY
    GROUPING SETS (
        (partner, last),
        (partner, last, id, day_date, number, payment_date)
    )
ORDER BY last DESC, partner, day_date DESC
"""
        return INVOICES
