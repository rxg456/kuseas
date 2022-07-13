from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'total': self.page.paginator.count,
                'page': self.page.number
            },
            'results': data,
        })