from rest_framework.pagination import PageNumberPagination

class OfferPagination(PageNumberPagination):
    """
    Custom pagination class for paginating offers.

    This class extends the `PageNumberPagination` provided by Django REST framework,
    allowing for pagination of offers with a default page size and the ability to
    adjust the page size through a query parameter.

    Attributes:
        page_size (int): The default number of items per page. In this case, it's set to 10 offers per page.
        page_size_query_param (str): The query parameter that allows the client to override the default page size.
            This is useful for pagination control via the URL, e.g., `?page_size=20` to display 20 offers per page.
    """
    
    page_size = 10
    """
    Defines the default page size for pagination. This value determines how many offers are displayed per page.
    In this case, the default is set to 10 offers per page.
    """

    page_size_query_param = "page_size"
    """
    Specifies the query parameter ('page_size') that allows the client to control the number of items per page.
    For example, a request like `?page_size=20` will return 20 offers per page instead of the default 10.
    """
