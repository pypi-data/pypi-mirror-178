import datetime
from collections import namedtuple


class Fund:
    """
    Details of a fund, including its current market price.
    
    Parameters
    ----------
    description : str
        Description of the fund, for example the name given by its provider.
    price : float, default 1.0
        Latest market price available for the fund.
    isin : str, default "None"
        If a real fund, the International Securities Identification Number
        (ISIN) of the fund should be specified.
        The ISIN is a unique 12-character alphanumerical identifier.
    date : datetime.date
        Date at which the `price` was last updated.
    
    Examples
    --------

    Constructing a Fund from a description and current price.
    
    >>> f = lisatools.Fund("FTSE Global All Cap Index Fund", 170.14)

    Constructing a Fund with all optional details.

    >>> f = lisatools.Fund("FTSE Global All Cap Index Fund", 170.14,
    ...                    isin="GB00BD3RZ582",
    ...                    date=datetime.date(2022, 11, 1))
    """

    def __init__(self,
                 description="Default fund",
                 price=1.0,
                 *,
                 isin="None",  # UNSPECIFIED9 is a valid ISIN
                 date=datetime.date.today()):
        self.description = description
        self.isin = isin   
        self.update_price(price, date=date)
    
    def __repr__(self):
        return (
            f"Fund({self.description!r}, {self.price!r}, "
            f"date={self.date!r}, isin={self.isin!r})"
        )
    
    def update_price(self, price, *, date=datetime.date.today()):
        """
        Set the price of the fund to a given value and optionally specify the
        date at which this price is correct.

        Parameters
        ----------
        price : float
            The new price of one unit of the fund.
        date : datetime.date, optional
            The date when the fund had the given price. If left unspecified, the
            date is set to the current one (at runtime).
        """
        self.price = price
        self.date = date
