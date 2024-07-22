from django.db.models import F, Sum, OuterRef

SumProduct = F("quantity") * F("price")


def get_totals(Model, targets, date_field=F("day__date"), filters=list()):
    return Model.objects.annotate(
        __date=date_field
    ).filter(
        *filters
    ).aggregate(**{
        attr: Sum(target)
        for attr, target in targets
    })


def get_totals_by_id(Model, groupby, target, date_field=F("day__date"), filters=list()):
    _id = f"{groupby}_id"
    return Model.objects.annotate(
        __date=date_field,
    ).values(_id).filter(*filters, **{
        _id: OuterRef("id")
    }).annotate(
        total=Sum(target)
    ).order_by(_id).values("total")
