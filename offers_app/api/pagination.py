from rest_framework.pagination import PageNumberPagination

class OfferPagination(PageNumberPagination):
    """
    Custom pagination for offers. Extends `PageNumberPagination` to allow pagination with a default page size
    and dynamic page size control via a query parameter.
    
    Attributes:
        page_size (int): Default number of offers per page (set to 6).
        page_size_query_param (str): Query parameter ('page_size') to allow clients to set their own page size.
    """
    
    page_size = 6
    page_size_query_param = "page_size"
