from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bookshop.views import BookViewSet, AuthorViewSet

routers = DefaultRouter()
routers.register("books", BookViewSet)
routers.register("authors", AuthorViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('books/<int:id>/buy/', BookViewSet.as_view({"post": "buy"}), name='book-buy'),
]
