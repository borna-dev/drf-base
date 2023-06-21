from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import get_object_or_404

from news.models import Article, Journalist, Comment
from news.api.serializer import ArticleSerializer, JournalistSerializer, CommentSerializer

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from rest_framework import permissions, authentication
from news.api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


# generic views
class JournalistList(generics.ListCreateAPIView):
    queryset = Journalist.objects.all()
    serializer_class = JournalistSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        pass


class JournalistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Journalist.objects.all()
    serializer_class = JournalistSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass


class ArticleList(generics.ListAPIView):
    queryset = Article.objects.order_by('id')
    serializer_class = ArticleSerializer
    pagination_class = None


class ArticleCreate(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        author_id = self.kwargs.get('author_id')
        serializer.save(author_id=author_id)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')

        has_comment = Comment.objects.filter(article_id=article_id, owner=self.request.user).exists()
        if has_comment:
            raise ValidationError('You already have a comment on this book')

        serializer.save(article_id=article_id, owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass


# class based views
class JournalistListCreateAPIView(APIView):

    def get(self, request):
        authors = Journalist.objects.all()
        serializer = JournalistSerializer(authors, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = JournalistSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleListCreateAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):

    def get_object(self, pk):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        return article

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        # article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# function based views
@api_view(['GET', 'POST'])
def article_list_create_api_view(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        # for data in serializer.data:
        #     data['sample'] = data['main_text'][:120] + '...'
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_api_view(request, pk):
    # article = get_object_or_404(Article, pk=pk)
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({'detail': f'{Article.__name__.lower()} with id {pk} not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # article.delete()
        return Response({'detail': f'{Article.__name__.lower()} with id {pk} has been deleted'}, status=status.HTTP_204_NO_CONTENT)
