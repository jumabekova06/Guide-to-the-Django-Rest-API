from rest_framework import viewsets
from . import models
from . import serializers
from .permissions import IsOwner
import pendulum
import django_filters
from rest_framework.decorators import action
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from dynamic_rest.viewsets import DynamicModelViewSet


class FriendViewset(NestedViewSetMixin, DynamicModelViewSet):
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


class BelongingViewset(DynamicModelViewSet):
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
    

class BorrowedViewset(NestedViewSetMixin, DynamicModelViewSet):
    queryset = models.Borrowed.objects.all().select_related("to_who", "what")
    permit_list_expands = ["what", "to_who"]
    serializer_class = serializers.BorrowedSerializer
    permission_classes = [IsOwner]
    filterset_class = BorrowedFilterSet

    @action(detail=True, url_path="remind", methods=["post"])
    def remind_single(self, request, *args, **kwargs):
        obj = self.get_object()
        send_mail(
            subject=f"Please return my belonging: {obj.what.name}",
            message=f'You forgot to return my belonging: "{obj.what.name}"" that you borrowed on {obj.when}. Please return it.',
            from_email="me@example.com",  # your email here
            recipient_list=[obj.to_who.email],
            fail_silently=False,
        )
        return Response("Email sent.")