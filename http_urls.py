from django.urls import path
from django.conf.urls import url

from rest_framework.routers import SimpleRouter

from buy_and_sell.views.sale_product_views import SaleProductList
from buy_and_sell.views.sale_product_views import SaleProductViewSet
from buy_and_sell.views.request_product_views import RequestProductList
from buy_and_sell.views.request_product_views import RequestProductViewSet
from buy_and_sell.views.payment_mode_views import PaymentModeViewSet
from buy_and_sell.views.categories import CategoriesViewSet
from buy_and_sell.views.search_view import GlobalSearchList
from buy_and_sell.views.who_am_i import WhoAmI
from buy_and_sell.views.picture_views import PictureList


app_name = 'buy_and_sell'
router = SimpleRouter()
router.register(
    r'sale_product',
    SaleProductViewSet,
    base_name='sale_product'
)
router.register(
    r'request_product',
    RequestProductViewSet,
    base_name='request_product'
)
router.register(
    r'payment',
    PaymentModeViewSet,
    base_name='payment_modes'
)
router.register(
    r'categories',
    CategoriesViewSet,
    base_name='categories'
)

urlpatterns = [
    url(r'^sale(/(?P<argument>[\w]+)/|/)?$', SaleProductList.as_view()),
    url(r'^sale(/(?P<argument>my_products)/|/)?$', SaleProductList.as_view()),
    url(r'^request(/(?P<argument>[\w]+)/|/)?$', RequestProductList.as_view()),
    url(r'^request(/(?P<argument>my_products)/|/)?$',
        RequestProductList.as_view()),
    url(r'^search/$', GlobalSearchList.as_view(), name="search"),
    path('who_am_i/', WhoAmI.as_view(), name='who_am_i'),
    path('picture/', PictureList.as_view(), name='product_picture'),
]

urlpatterns += router.urls
