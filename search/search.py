from components import User, Station, Gaz
from search_utils.xml_parser_utils import XMLParser
from search_utils.io_utils import IOUtils

import datetime
import logging
import time
from xml.etree.cElementTree import Element
from haversine import haversine


class Search:
    """
    Class used to execute the search of the best stations for the user

    Attributes
    ----------
    TOP_N_STATIONS: int
        Maximum number of stations to keep
    HAVERSINE: Haversine
        Used to compute haversine distance
    """

    TOP_N_STATIONS = 10
    HAVERSINE = haversine.Haversine()

    @classmethod
    def process_station(cls, user: User, element: Element) -> Station:
        """
        Extract a station from the input data
        If the attribute extracted are well formatted, a station
        is created and the distance with the user position is computed
        Else print a message to warn about the wrong format

        :param user:    the user attributes requesting the stations
        :param element: the current element containing a station
        :return: the created station
        """
        station = Station(id=element.attrib[XMLParser.ID_IDENTIFIER])

        lat = element.attrib[XMLParser.LATITUDE_IDENTIFIER]
        lon = element.attrib[XMLParser.LONGITUDE_IDENTIFIER]

        if (Station.validate_coordonate(coordonate=lat) and Station.validate_coordonate(coordonate=lon)):

            lat = Station.format_coordonate(coordonate=lat)
            lon = Station.format_coordonate(coordonate=lon)

            station_location = (lat, lon)
            user_location = user.get_position()

            distance = cls.HAVERSINE.distance(user_location, station_location)

            station.latitude = lat
            station.longitude = lon
            station.distance = distance

        else:

            logging.warning("Wrong attributes for station id {id}: (lat:'{lat}', lon:'{lon}')".format(
                id=station.id, lat=lat, lon=lon))

        return station

    @classmethod
    def process_price(cls, element: Element, station: Station, requested_gaz: Gaz, user: User) -> Station:
        """
        Extract the price from the input data
        Check the date of the price and the gaz type match with the user request
        If the dates and the types match, the price is added to the currently extrated station

        :param element:       the current element containing a price
        :param station:       the currently extracted station
        :param requested_gaz: the gaz type requested by the user
        :param user:          the user attributes requesting the stations
        :return: the currently extracted station with the right price
        """
        if element.attrib.get(XMLParser.UPDATE_IDENTIFIER):

            price_updated_date = element.attrib.get(XMLParser.UPDATE_IDENTIFIER)

            price_date = datetime.datetime \
                .strptime(price_updated_date, XMLParser.DATE_FORMAT) \
                .replace(hour=0, minute=0, second=0)

            price_gaz_type = int(element.attrib[XMLParser.ID_IDENTIFIER])

            if user.date == price_date and price_gaz_type == requested_gaz.id:

                station.price = float(element.attrib[XMLParser.PRICE_VALUE_IDENTIFIER])

        return station

    @classmethod
    def validate_station(cls, station: Station) -> bool:
        """
        Check a station are the right attributes filled in before adding it the list of stations
        Return True if the station:
          - is defined
          - has a price extracted from the input data
          - has a distance computed using the input data

        :param station: the current station being processed
        :return: True if the station can be added to the list of station, False otherwise
        """

        return station is not None and station.price is not None and station.distance is not None

    @classmethod
    def process_data(cls, data, user: User, requested_gaz: Gaz) -> dict:
        """
        Process the rows of the input data
        Create a station and add it the list of stations to keep if the required attributes are well filled in

        :param data:          the streamed input data
        :param user:          the user attributes requesting the stations
        :param requested_gaz: the gaz type requested by the user
        :return: a dictionary containing the stations with the station id as key and the station as value
        """

        stations_to_keep = {}

        current_station = None

        for event, element in data:

            if event == XMLParser.START_EVENT and element.tag == XMLParser.STATION_IDENTIFIER:

                current_station = cls.process_station(user=user, element=element)

            if event == XMLParser.START_EVENT and element.tag == XMLParser.PRICE_IDENTIFIER:

                current_station = cls.process_price(element=element, station=current_station,
                                                    requested_gaz=requested_gaz, user=user)

            if cls.validate_station(station=current_station):

                stations_to_keep[current_station.id] = current_station

            element.clear()

        return stations_to_keep

    @classmethod
    def get_eligible_stations(cls, user: User, stations: dict) -> filter:
        """
        Keep the stations located in the user area
        To be considered in the user area, the station distance to the user needs to be inside the user radius

        :param user:     the user attributes requesting the stations
        :param stations: the dictionary containing the kept stations
        :return: a list of stations inside the user area
        """
        return filter(lambda d: d[1].distance <= user.radius, stations.items())

    @classmethod
    def get_sorted_stations(cls, stations: list) -> list:
        """
        Sort a list of tuple (id, station) depending on:
          - the price
          - the distance to the user in case of price tie

        :param stations: the list of stations
        :return: a sorted list of stations
        """
        return sorted(stations, key=lambda station: (station[1].price, station[1].distance))

    @classmethod
    def get_n_first_stations(cls, n: int, stations: list) -> list:
        """
        Return the n top element of the list

        :param n:        the number of stations to keep
        :param stations: the list of stations
        :return: the n top stations
        """
        return stations[:n]

    @classmethod
    def find_stations(cls, user: User, stations: dict) -> list:
        """
        Execute the station search according to the user attributes

        :param user:     the user attributes requesting the stations
        :param stations: the dictionary containing the kept stations
        :return: the top n station sorted by price inside the user area
        """
        filtered_stations = cls.get_eligible_stations(user=user, stations=stations)
        sorted_stations = cls.get_sorted_stations(stations=filtered_stations)
        selected_stations = cls.get_n_first_stations(n=cls.TOP_N_STATIONS, stations=sorted_stations)
        return selected_stations

    @classmethod
    def format_output(cls, gaz: Gaz, stations: Station) -> dict:
        """
        Prepare the output stations in the right format to write them in JSON later.
        Add the postion of the station to get the rank.

        :param gaz:      the gaz type requested by the user
        :param stations: the list of station kept after all the process
        :return: the data formatted as dictionary (JSON style)
        """
        stations_to_keep = []

        for index, (_, station) in enumerate(stations):
            stations_to_keep.append({
                "latitude": station.latitude,
                "longitude": station.longitude,
                "price": station.price,
                "distance": round(station.distance, 2),
                "rank": index + 1,
            })

        result = {
            "name": gaz.gaz_type,
            "stations": stations_to_keep,
        }

        return result

    @classmethod
    def run(cls, args, ressources_path: str, output_path: str):
        """Execute the sear to find the top best gaz stations matching the user request"""

        load_start_time = time.time()

        user = User(latitude=args.latitude, longitude=args.longitude, radius=args.radius,
                    date=args.date, gaz_type=args.gaz_type)

        gaz = Gaz(gaz_type=args.gaz_type)

        station_data = XMLParser.load_data(path=ressources_path)

        extracted_stations = cls.process_data(data=station_data, user=user, requested_gaz=gaz)

        execution_time = (time.time() - load_start_time) * 1000
        logging.warning("--- {time} ms for data loading---".format(time=execution_time))

        search_start_time = time.time()

        valid_stations = cls.find_stations(user=user, stations=extracted_stations)

        execution_time = (time.time() - search_start_time) * 1000
        logging.warning("--- {time} ms for search---".format(time=execution_time))

        result = cls.format_output(gaz=gaz, stations=valid_stations)

        IOUtils.json_writer(path=output_path, data=result)

    @staticmethod
    def main(args):
        ressources_path = "ressources/oil_data/PrixCarburants_annuel_2022.xml"
        output_ppath = "outputs/results.json"

        Search.run(args=args, ressources_path=ressources_path, output_path=output_ppath)
