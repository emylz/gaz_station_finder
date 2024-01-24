from search.components import User, Station, Gaz, Coordinate

import datetime
import pytest
import argparse


class TestUser:

    @pytest.fixture
    def get_user(self):
        """Provide a base user for all user test functions"""
        return User(latitude=-52.0000, longitude=0.12345678,
                    radius=1500, date=datetime.datetime(year=2024, month=1, day=21),
                    gaz_type="SP98")

    def test_user(self, get_user):
        """Test user attributes are formatted as expected"""

        assert get_user.latitude == -52.0000
        assert get_user.longitude == 0.12345678
        assert get_user.radius == 1.5
        assert get_user.date == datetime.datetime(year=2024, month=1, day=21)
        assert get_user.gaz_type == "SP98"

    def test_get_position(self, get_user):
        """Test user position is formatted as expected"""

        assert get_user.get_position() == (-52.0, 0.12345678)


class TestStation:

    @pytest.fixture
    def get_station(self):
        """Provide a base station for all station test functions"""
        return Station(id=1)

    def test_station(self, get_station):
        """Test stations attributes are formatted as expected"""

        assert get_station.id == 1
        assert get_station.latitude is None
        assert get_station.longitude is None
        assert get_station.distance is None
        assert get_station.price is None

    def test_validate_coordonate_regular(self):
        """Test a regular integer coordinate is validated"""

        assert Station.validate_coordonate("12") is True

    def test_validate_coordonate_negative(self):
        """Test a negative integer coordinate is validated"""

        assert Station.validate_coordonate("-12") is True

    def test_validate_coordonate_decimal(self):
        """Test a decimal coordinate is validated"""

        assert Station.validate_coordonate("12.3") is True

    def test_validate_coordonate_decimal_negative(self):
        """Test a negative decimal coordinate is validated"""

        assert Station.validate_coordonate("-12.3") is True

    def test_validate_coordonate_empty(self):
        """Test an empty sting coordinate is not validated"""

        assert Station.validate_coordonate("") is False

    def test_validate_coordonate_w_letter(self):
        """Test a mix of numbers and letters coordinate is not validated"""

        assert Station.validate_coordonate("123e7") is False

    def test_format_coordonate_decimal(self):
        """Test a decimal coordinate is formatted as expected"""

        assert Station.format_coordonate("8900000.087") == 89.00000087

    def test_format_coordonate_integer(self):
        """Test an integer coordinate is formatted as expected"""

        assert Station.format_coordonate("6500000") == 65.00000


class TestGaz:

    @pytest.fixture
    def get_gaz(self):
        """Provide a base gaz for all gaz test functions"""
        return Gaz(gaz_type="E10")

    def test_gaz(sel, get_gaz):
        """Test gaz attributes are formatted as expected"""

        assert get_gaz.gaz_type == "E10"
        assert get_gaz.id == 5


class TestCoordinate:

    def test_validate_latitude(self):
        """Test the latitude argument is parsed as expected"""

        assert Coordinate.validate_latitude("90") == 90.0

    def test_validate_latitude_exception(self):
        """Test an exception is raised when the latitude is outside of the boundaries"""

        with pytest.raises(argparse.ArgumentTypeError) as error:
            argparse.ArgumentTypeError, Coordinate.validate_latitude("-91.0")

        assert str(error.value) == "Latitude value is incorrect. Value expects [-90: 90]. Found: -91.0"

    def test_validate_latitude_string_exception(self):
        """Test an exception is raised when the latitude cannot be cast to a float"""

        with pytest.raises(argparse.ArgumentTypeError) as error:
            argparse.ArgumentTypeError, Coordinate.validate_latitude("72e1.02")

        assert str(error.value) == "Wrong value format for latitude. Expects a float value."

    def test_validate_longitude(self):
        """Test the longitude argument is parsed as expected"""

        assert Coordinate.validate_longitude("-180.0") == -180.0

    def test_validate_longitude_exception(self):
        """Test an exception is raised when the latitude is outside of the boundaries"""

        with pytest.raises(argparse.ArgumentTypeError) as error:
            argparse.ArgumentTypeError, Coordinate.validate_longitude("190.9")

        assert str(error.value) == "Longitude value is incorrect. Value expects [-180: 180]. Found: 190.9"

    def test_validate_longitude_string_exception(self):
        """Test an exception is raised when the longitude cannot be cast to a float"""

        with pytest.raises(argparse.ArgumentTypeError) as error:
            argparse.ArgumentTypeError, Coordinate.validate_longitude("-999e.099")

        assert str(error.value) == "Wrong value format for longitude. Expects a float value."
