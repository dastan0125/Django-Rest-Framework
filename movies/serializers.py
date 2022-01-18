from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    class Meta:
        model = Movie
        fields = ('title', "tagline", 'category')



class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""

    class Meta:
        model = Review
        fields = ('name', 'text', 'parent')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewCreateSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft', )


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating
