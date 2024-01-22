import datetime


class User:
    """
    Represent the params set as input by the user

    Attributes
    ----------
    latitude: float
        latitue of the user
    longitude: float
        longitude of the user
    radius: float
        radius maximum inside a station needs to be (in km)
    date: datetime
        date of the request by the user
    gaz_type: float
        requested gaz type
    """

    __slots__ = "latitude", "longitude", "radius", "date", "gaz_type"

    def __init__(self, latitude: float, longitude: float, radius: float, date: datetime, gaz_type: str) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius / 1000
        self.date = date
        self.gaz_type = gaz_type

    def get_position(self):
        """Return a tuple representing the user geolocation position"""
        return (self.latitude, self.longitude)


class Station:
    """
    Represent a station extracted from the parsed data

    Attributes
    ----------
    id: int
        id of the station
    latitude: float
        latitude of the station
    longitude: float
        longitude of the station
    distance: datetime
        distance between the user and the station
    price: float
        price of the requested gaz for the given date
    """

    __slots__ = "id", "latitude", "longitude", "distance", "price"

    def __init__(self, id: str, latitude: float = None, longitude: float = None,
                 distance: float = None, price: float = None) -> None:

        self.id = int(id)
        self.latitude = latitude
        self.longitude = longitude
        self.distance = distance
        self.price = price

    @staticmethod
    def validate_coordonate(coordonate: str) -> bool:
        """
        Check inpute coordonate is well formatted

        e.g.:
          - "" will return False
          - "123e" will return False
          - "123" will return True
          - "-123" will return True
        """
        return coordonate.lstrip('-').replace('.', '').isdigit()

    @staticmethod
    def format_coordonate(coordonate: str) -> float:
        """Format inpute coordonate to the expected format"""
        return float(coordonate) / 100000


class Gaz:
    """
    Represent the requested gaz type by the user

    Attributes
    ----------
    id: int
        id of the requested gaz to match with the input data
    gaz_type: str
        requested gaz type
    """

    GAZ_MAPPING = {
        "Gazole": 1,
        "SP95": 2,
        "E85": 3,
        "GPLc": 4,
        "E10": 5,
        "SP98": 6,
    }

    def __init__(self, gaz_type: str):
        self.gaz_type = gaz_type
        self.id = Gaz.GAZ_MAPPING[gaz_type]
