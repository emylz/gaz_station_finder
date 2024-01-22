from search.search import Search
from search.search_utils.xml_parser_utils import XMLParser
from search.components import User, Station, Gaz

import pytest
import datetime


class XMLElement:
    """Class used to mock XML Element objects"""

    def __init__(self, tag, attrib):
        self.tag = tag
        self.attrib = attrib


class TestSearch:

    @pytest.fixture
    def get_user(self):
        """Provide a base user for all search test functions"""

        return User(latitude=13.0001, longitude=-89.0987652,
                    radius=1500, date=datetime.datetime(year=2024, month=1, day=21),
                    gaz_type="SP98")

    @pytest.fixture
    def get_station_element(self):
        """Provide a base station element for all search test functions"""

        attrib = {
            XMLParser.ID_IDENTIFIER: "750002001",
            XMLParser.LATITUDE_IDENTIFIER: "1288888",
            XMLParser.LONGITUDE_IDENTIFIER: "-8909888",
        }
        tag = XMLParser.STATION_IDENTIFIER
        return XMLElement(tag=tag, attrib=attrib)

    @pytest.fixture
    def get_price_element(self):
        """Provide a base price element for all search test functions"""

        attrib = {
            XMLParser.PRICE_VALUE_IDENTIFIER: "1.999",
            XMLParser.UPDATE_IDENTIFIER: "2024-01-21T00:00:00",
            XMLParser.ID_IDENTIFIER: "6",
        }
        tag = XMLParser.PRICE_IDENTIFIER
        return XMLElement(tag=tag, attrib=attrib)

    @pytest.fixture
    def get_gaz(self):
        """Provide a base gaz for all search test functions"""

        return Gaz(gaz_type="SP98")

    @pytest.fixture
    def get_station(self):
        """Provide a base station for all search test functions"""

        return Station(id=1, latitude=98.2, longitude=75.999,
                       distance=1.39)

    def test_process_station(self, get_user, get_station_element):
        """Test the attributes are set to the station as expected"""

        station = Search().process_station(user=get_user, element=get_station_element)

        assert station.latitude == 12.88888
        assert station.longitude == -89.09888
        assert station.distance == 12.367105998856639

    def test_process_station_none(self, get_user, get_station_element):
        """Test the attributes are None when the format of the input attributes is wrong"""

        element = get_station_element
        element.attrib[XMLParser.LATITUDE_IDENTIFIER] = ""
        station = Search().process_station(user=get_user, element=element)

        assert station.latitude is None
        assert station.longitude is None
        assert station.distance is None

    def test_process_price(self, get_price_element, get_station, get_gaz, get_user):
        """Test the price is added to the station as expected"""

        station = Search().process_price(element=get_price_element, station=get_station,
                                         requested_gaz=get_gaz, user=get_user)

        assert station.price == 1.999

    def test_process_price_none(self, get_price_element, get_station, get_gaz, get_user):
        """Test the price is None when there is not the right information inpute"""

        get_gaz.id = 5
        station = Search().process_price(element=get_price_element, station=get_station,
                                         requested_gaz=get_gaz, user=get_user)

        assert station.price is None

    def test_validate_station(self, get_station):
        """Test the station is validated as expected"""

        station = get_station
        station.price = 1.59

        assert Search().validate_station(station=station) is True

    def test_validate_station_none(self, get_station):
        """Test the station is not validated as expected"""

        assert Search().validate_station(station=get_station) is False

    def test_get_eligible_stations(self, get_user):
        """Test the number of stations kept as expected"""

        stations = {
            1: Station(id=1, distance=0.987),
            2: Station(id=2, distance=1.49),
            3: Station(id=3, distance=1.51),
            4: Station(id=4, distance=12.89),
        }
        result = list(Search().get_eligible_stations(user=get_user, stations=stations))

        assert len(result) == 2

    def test_get_sorted_stations(self):
        """Test the order of the stations according to their attributes is as expected"""

        stations = [
            (1, Station(id=1, distance=0.987, price=2.01)),
            (2, Station(id=2, distance=1.49, price=1.988)),
            (3, Station(id=3, distance=1.51, price=1.988)),
        ]
        result = [station for _, station in Search().get_sorted_stations(stations=stations)]

        assert result[0].id == 2
        assert result[1].id == 3
        assert result[2].id == 1

    def test_get_n_first_stations(self):
        """Test the final number of station specified is kept as expected"""

        stations = [
            (1, Station(id=1, distance=0.987, price=1.78)),
            (2, Station(id=2, distance=1.49, price=1.999)),
            (3, Station(id=3, distance=1.51, price=1.999)),
        ]
        result = [station for _, station in Search().get_n_first_stations(n=2, stations=stations)]

        assert result[0].id == 1
        assert result[1].id == 2
        assert len(result) == 2
