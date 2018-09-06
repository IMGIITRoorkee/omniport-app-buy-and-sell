from kernel.admin.site import omnipotence

from buy_and_sell.models import (
    SaleProduct,
    RequestProduct,
    Category,
    PaymentMode,
    Picture
)

omnipotence.register(SaleProduct)
omnipotence.register(RequestProduct)
omnipotence.register(Category)
omnipotence.register(PaymentMode)
omnipotence.register(Picture)