from categories.serializers import CategorySerializer
from platforms.serializers import PlatformSerializer
from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


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
            'price': float(instance.price),
            'stock': instance.stock,
            'released_at': instance.released_at,
            'pegi': instance.get_pegi_display(),
            'category': CategorySerializer(instance.category, request=self.request).serialize(),
            'platforms': PlatformSerializer(
                instance.platforms.all(), request=self.request
            ).serialize(),
        }


class ReviewSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'rating': instance.rating,
            'comment': instance.comment,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.author, request=self.request).serialize(),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
