

from django.utils.translation import gettext_lazy as _


class Base(object):
    code = ""
    message = ""
    dispatch_date = None

    @property
    def short_message(self):
        return self.message

    @property
    def is_available_to_buy(self):
        return self.is_purchase_permitted(1)[0]

    def is_purchase_permitted(self, quantity):

        return False, _("unavailable")


class Unavailable(Base):

    code = "unavailable"
    message = _("Unavailable")


class Available(Base):

    code = "available"
    message = _("Available")

    def is_purchase_permitted(self, quantity):
        return True, ""


class StockRequired(Base):

    CODE_IN_STOCK = "instock"
    CODE_OUT_OF_STOCK = "outofstock"

    def __init__(self, num_available):
        self.num_available = num_available

    def is_purchase_permitted(self, quantity):
        if self.num_available <= 0:
            return False, _("no stock available")

        if quantity > self.num_available:
            msg = _("a maximum of %(max)d can be bought") % {"max": self.num_available}
            return False, msg
        return True, ""

    @property
    def code(self):

        if self.num_available > 0:
            return self.CODE_IN_STOCK
        return self.CODE_OUT_OF_STOCK

    @property
    def short_message(self):
        if self.num_available > 0:

            return _("In stock")
        return _("Unavailable")

    @property
    def message(self) -> str:

        if self.num_available > 0:
            return _("In stock (%d available)") % self.num_available
        return _("Unavailable")
