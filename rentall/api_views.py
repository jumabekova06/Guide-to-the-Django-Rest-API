from rest_framework import viewsets
from . import models
from . import serializers
from .permissions import IsOwner
import pendulum

class FriendViewset(viewsets.ModelViewSet):
    queryset = models.Friend.objects.all()
    serializer_class = serializers.FriendSerializer
    permission_classes = [IsOwner]
    # and so on…
    def get_queryset(self):
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

class BorrowedViewSet(viewsets.ModelViewSet):
    queryset = models.Borrowed.objects.all()
    serializer_class = serializers.BorrowedSerializer