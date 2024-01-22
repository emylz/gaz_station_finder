import json


class IOUtils:

    @staticmethod
    def json_writer(path: str, data: dict) -> None:
        """
        Write a json file with dictionary as input.
        Overwrite the file if already exists

        :param str:  path where to write the file
        :param data: data to write
        """

        with open(path, "w+") as file:
            json.dump(data, file)
