from rest_framework import serializers
from django.utils.timezone import now, timedelta
from django.utils.timesince import timesince
from news.models import Article, Journalist, Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Comment
        exclude = ['article']


class ArticleSerializer(serializers.ModelSerializer):
    days_since_published = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)
    # author_fname = serializers.ReadOnlyField(source='author.name')
    # author_surname = serializers.ReadOnlyField(source='author.surname')

    class Meta:
        model = Article
        fields = "__all__"
        # fields = ['id', 'title']
        # exclude = ['author']

    def get_days_since_published(self, obj):
        # obj.published_time = (now() - timedelta(days=7)).date()
        return timesince(obj.published_time, now().date())

    def validate_published_time(self, value):
        if value > now().date():
            raise serializers.ValidationError('This date has not come yet')
        return value

    def validate_main_text(self, value):
        if len(value) < 20:
            raise serializers.ValidationError('Dude please make more details!')
        return value


class JournalistSerializer(serializers.ModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='article-detail')
    # articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Journalist
        fields = "__all__"


# using basic serializer
class ArticleSerializerDefault(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, label='dude_id')
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    main_text = serializers.CharField()
    published_time = serializers.DateField()
    active = serializers.BooleanField(source='is_active')
    created_time = serializers.DateTimeField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        # return { 'main_text' : instance.main_text }
        ret = super().to_representation(instance)
        ret['summary'] = ret['main_text'][:120] + '...'
        return ret

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.main_text = validated_data.get('main_text', instance.main_text)
        instance.published_time = validated_data.get('published_time', instance.published_time)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def validate_author(self, value):
        if value.lower().startswith('x'):
            raise serializers.ValidationError('Dude you can\'t use xName for an author!')
        return value

    def validate(self, data):
        if len(data['main_text']) < 20:
            raise serializers.ValidationError('Dude please make more details!')
        if data['author'] == data['title']:
            raise serializers.ValidationError('Dude this book is too narcissistic')
        return data
