from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    """
    Класс для пагинации
    """
    page_size = 10
