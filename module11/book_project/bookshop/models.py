from django.db import models, transaction


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    count = models.IntegerField(default=0)

    @staticmethod
    @transaction.atomic
    def buy(book_id: int) -> 'Book':
        """ Метод для покупки книги, типа снижает count на 1, если он есть. """
        book = Book.objects.select_for_update().filter(id=book_id, count__gt=0).first()

        if not book:
            raise ValueError("Не получилось продать книгу, видимо нет в наличии.")

        book.count -= 1
        book.save()
        return book
