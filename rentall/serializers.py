from rest_framework import serializers
from . import models
import pendulum

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from . import models
class FriendSerializer(FlexFieldsModelSerializer):
    owner = serializers.HiddenField(
            default=serializers.CurrentUserDefault())
    class Meta:
        model = models.Friend
        fields = ('id', 'name', 'owner', 'has_overdue')

    def get_has_overdue(self, obj):
        if hasattr(obj, 'ann_overdue'):
            return obj.ann_overdue
        return obj.borrowed_set.filter(returned__isnull=True, when=pendulum.now().subtract(months=2)).exists()
        
class BelongingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Belonging
        fields = ('id', 'name')


class BorrowedSerializer(FlexFieldsModelSerializer):
    expandable_fields = {
        "what": (BelongingSerializer),
        "to_who": (FriendSerializer),
    }

    class Meta:
        model = models.Borrowed
        fields = ("id", "what", "to_who", "when", "returned")