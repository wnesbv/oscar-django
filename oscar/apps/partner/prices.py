

from oscar.core import prices


class Base(object):

    exists = False
    is_tax_known = False
    excl_tax = None
    incl_tax = None

    @property
    def effective_price(self):
        return self.excl_tax

    tax = None
    retail = None
    currency = None

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)


class Unavailable(Base):
    pass


class FixedPrice(Base):

    exists = True

    def __init__(self, currency, excl_tax, tax=None):
        self.currency = currency
        self.excl_tax = excl_tax
        self.tax = tax

    @property
    def incl_tax(self):
        if self.is_tax_known:
            return self.excl_tax + self.tax
        raise prices.TaxNotKnown(
            "Can't calculate price.incl_tax as tax isn't known")

    @property
    def is_tax_known(self) -> bool:
        return self.tax is not None


class TaxInclusiveFixedPrice(FixedPrice):

    exists = is_tax_known = True

    def __init__(self, currency, excl_tax, tax):
        self.currency = currency
        self.excl_tax = excl_tax
        self.tax = tax

    @property
    def incl_tax(self):
        return self.excl_tax + self.tax

    @property
    def effective_price(self):
        return self.incl_tax
