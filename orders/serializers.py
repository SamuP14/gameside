from shared.serializers import BaseSerializer


class OrderSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.status,
            'key': instance.key,
            'user': BaseSerializer.serialize(instance.user),
            'game': BaseSerializer.serialize(instance.game),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
