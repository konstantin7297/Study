from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from bookshop.models import Book, Author
from bookshop.serializers import BookSerializer, AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """ Класс создающий основные CRUD для работы с книгами. """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'put']

    @action(detail=True, methods=['post'], url_name="book-buy")
    def buy(self, request: Request, *args, **kwargs) -> Response:
        """ Метод для покупки книги: снижение count или ошибка. """
        try:
            updated_book = Book.buy(book_id=kwargs.get("pk"))
            return Response(BookSerializer(updated_book).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AuthorViewSet(viewsets.ModelViewSet):
    """ Класс создающий основные CRUD для работы с авторами. """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post', 'put']
