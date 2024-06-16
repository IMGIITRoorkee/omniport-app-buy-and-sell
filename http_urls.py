from django.urls import path, re_path ,include,URLPattern
from rest_framework.routers import SimpleRouter
from buy_and_sell.views.sale_product_views import SaleProductList
from buy_and_sell.views.constants import ConstantViewSet
from buy_and_sell.views.sale_product_views import SaleProductViewSet
from buy_and_sell.views.request_product_views import RequestProductList
from buy_and_sell.views.request_product_views import RequestProductViewSet
from buy_and_sell.views.payment_mode_views import PaymentModeViewSet
from buy_and_sell.views.categories import CategoriesViewSet
from buy_and_sell.views.search_view import GlobalSearchList
from buy_and_sell.views.who_am_i import WhoAmI
from buy_and_sell.views.picture_views import PictureList
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

app_name = 'buy_and_sell'
router = SimpleRouter()
router.register(
    r'sale_product',
    SaleProductViewSet,
    basename='sale_product'
)
router.register(
    r'request_product',
    RequestProductViewSet,
    basename='request_product'
)
router.register(
    r'payment',
    PaymentModeViewSet,
    basename='payment_modes'
)
router.register(
    r'categories',
    CategoriesViewSet,
    basename='categories'
)
router.register(
    r"constants", 
    ConstantViewSet, 
    basename="constant",
)

urlpatterns = [
    re_path(r'^sale/category((?P<argument>[\w]+)/|/)filter(?P<filter_slug>[\w]+)?$', SaleProductList.as_view()),
    re_path(r'^sale(/(?P<argument>my_products)/|/)?$', SaleProductList.as_view()),
    re_path(r'^request(/(?P<argument>[\w]+)/|/)?$', RequestProductList.as_view()),
    re_path(r'^request(/(?P<argument>my_products)/|/)?$',
        RequestProductList.as_view()),
    re_path(r'^search/$', GlobalSearchList.as_view(), name="search"),
    path('who_am_i/', WhoAmI.as_view(), name='who_am_i'),
    path('picture/', PictureList.as_view(), name='product_picture'),
    path('', include(router.urls)),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns,
    
)
urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

