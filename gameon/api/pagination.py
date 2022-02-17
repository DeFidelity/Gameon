from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'sheet'

class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'list'
    offset_query_param = 'start'

    class WatchListCursorPagination(CursorPagination):
        page_size = 5

        ordering = 'created'