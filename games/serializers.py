from shared.serializers import BaseSerializer


class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url),
            'price': instance.price,
            'stock': instance.stock,
            'released_at': instance.released_at,
            'pegi': instance.pegi,
            'category': BaseSerializer.serialize(instance.category),
            'platforms': BaseSerializer.serialize(instance.platforms),
        }


class ReviewSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'rating': instance.rating,
            'comment': instance.comment,
            'game': BaseSerializer.serialize(instance.game),
            'author': BaseSerializer.serialize(instance.author),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
