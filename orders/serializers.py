from games.serializers import GameSerializer
from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


class OrderSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'key': instance.key if instance.get_status_display() == 'PAID' else None,
            'user': UserSerializer(instance.user, request=self.request).serialize(),
            'games': GameSerializer(instance.games.all(), request=self.request).serialize(),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'price': instance.price,
        }
