import xml.etree.cElementTree as xmlReader


class XMLParser:

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    START_EVENT = "start"
    END_EVENT = "end"
    STATION_IDENTIFIER = "pdv"
    PRICE_IDENTIFIER = "prix"
    LATITUDE_IDENTIFIER = "latitude"
    LONGITUDE_IDENTIFIER = "longitude"
    ID_IDENTIFIER = "id"
    PRICE_VALUE_IDENTIFIER = "valeur"
    UPDATE_IDENTIFIER = "maj"

    @staticmethod
    def load_data(path: str):
        """
        Return an generator of the XML path given in param
        :param path: the XML path
        :return: the generator with the data
        """
        return xmlReader.iterparse(path, events=("start", "end"))
