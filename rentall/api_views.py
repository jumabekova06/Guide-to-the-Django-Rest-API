from rest_framework import viewsets
from . import models
from . import serializers
from .permissions import IsOwner
import pendulum
import django_filters


class FriendViewset(viewsets.ModelViewSet):
    queryset = models.Friend.objects.all()
    serializer_class = serializers.FriendSerializer
    permission_classes = [IsOwner]
    # and so on…
    def get_queryset(self):
        from django.db import models

        return super().get_queryset().annotate(ann_overdue=models.Case(
            models.When(borrowed__when__lte=pendulum.now().subtract(months=2),
                then=True),
            default=models.Value(False),
            output_field=models.BooleanField()
             )
        )

class BelongingViewset(viewsets.ModelViewSet):
    queryset = models.Belonging.objects.all()
    serializer_class = serializers.BelongingSerializer
    permission_classes = [IsOwner]

class BorrowedFilterSet(django_filters.FilterSet):
    missing = django_filters.BooleanFilter(field_name="returned", lookup_expr="isnull")
    overdue = django_filters.BooleanFilter(method="get_overdue", field_name="returned")

    class Meta:
        model = models.Borrowed
        fields = ["what", "to_who", "missing", "overdue"]

    def get_overdue(self, queryset, field_name, value):
        if value:
            return queryset.overdue()
        return queryset

class BorrowedViewset(viewsets.ModelViewSet):
    queryset = models.Borrowed.objects.all()
    serializer_class = serializers.BorrowedSerializer
    permission_classes = [IsOwner]
    filterset_fields = {
        'returned': ['exact', 'lte', 'gte', 'isnull']
        } # here

    def get_queryset(self):
        qs = super().get_queryset()
        only_missing = str(self.request.query_params.get('missing')).lower()
        if only_missing in ['true', '1']:
            return qs.filter(returned__isnull=True)
        return qs
