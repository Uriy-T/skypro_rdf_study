from rest_framework.pagination import PageNumberPagination

class CoursesPagination(PageNumberPagination):
    """
    Пагинация списка курсов
    """
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class LessonsPagination(PageNumberPagination):
    """
    Пагинация списка уроков
    """
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2

