from rest_framework.pagination import CursorPagination, PageNumberPagination


class CustomCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-id'

class SubTaskPagination(PageNumberPagination):
    page_size = 5