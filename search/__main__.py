import argparse
import datetime
from search import Search
from components import Coordinate

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='FindBestStation',
                                     description='Return the top N number of cheapest gaz station near you')
    parser.add_argument('--latitude', help='You current latitue',
                        required=True, type=Coordinate.validate_latitude)
    parser.add_argument('--longitude', help='Your current longitude',
                        required=True, type=Coordinate.validate_longitude)
    parser.add_argument('--radius', help='Your current radius', required=True, type=float)
    parser.add_argument('--date', help="Today's date, format yyyy-MM-dd", required=True,
                        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    parser.add_argument('--gaz_type', help='Requested gaz type',
                        choices=['Gazole', 'SP95', 'SP98', 'GPLc', 'E10', 'E85'],
                        required=True)
    args = parser.parse_args()

    Search.main(args)
