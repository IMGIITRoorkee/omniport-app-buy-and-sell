from django.urls import path
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from buy_and_sell.views.sale_product_views import SaleProductList
from buy_and_sell.views.picture_views import PicturesList
from buy_and_sell.views.sale_product_views import SaleProductViewSet
from buy_and_sell.views.payment_mode_views import PaymentModeViewSet

app_name = 'buy_and_sell'
router = DefaultRouter()
router.register(r'sale_product', SaleProductViewSet, base_name='sale_product')
router.register(r'payment', PaymentModeViewSet, base_name='payment_modes')

urlpatterns = [
    url(r'^sale(/(?P<argument>[\w]+)/|/)?$', SaleProductList.as_view()),
    url(r'^sale(/(?P<argument>my_products)/|/)?$', SaleProductList.as_view()),
    url(r'^picture/$', PicturesList.as_view()),
]

urlpatterns += router.urls
