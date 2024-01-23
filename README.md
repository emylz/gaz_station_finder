# Gaz station finder

This program helps you to find the cheapest gaz station around you and within a specified area.

To execute the search you need to download the xml data available [here](https://donnees.roulez-eco.fr/opendata/annee/2022), unzip it and put the xml file inside the folder *ressources/oil_data*. The file needs to be named *PrixCarburants_annuel_2022.xml*.

The result will be a JSON file inside the folder *outputs* and called *results.json*.

If you want to use different names feel free to rename the names in the code as well.

> :warning: **Important: the Python version used is Python3.9**.

## How to run

First, clone the project.

### On Windows

Open a Windows CMD and go to the project directory:

```C:/ cd C:/path/to/project/gaz_station_finder```

Optionnal: Activate the Python virtual environnement. This step is not mandatory. **You need to have you own virtual environnement set up**.

```C:/path/to/project/gaz_station_finder> venv\Scripts\activate```

Install the requirements:

```(venv) C:/path/to/project/gaz_station_finder> pip install -r requirements.txt```

Launch the search:

 ```(venv) C:/path/to/project/gaz_station_finder> python3 ./search --latitude=48.8319929 --longitude=2.3245488 --radius=5000 --date=2022-02-21 --gaz_type=SP98```

 - latitude: the latitude where the user is located.
 - longitude: the longitude where the user is located.
 - radius: the area in which the station must be (in meter).
 - date: date of the request. Prices will be filtered according to the date.
 - gaz_type: the gaz type requested. Prices checked will be according to the requested gaz type.

 Execute the tests:

 Set the PYTHONPATH to the current directory:

 ```(venv) C:/path/to/project/gaz_station_finder> set PYTHONPATH=C:/path/to/project/gaz_station_finder/search```

 Then you can run them:

 ```(venv) C:/path/to/project/gaz_station_finder> python3 -m pytest tests```

### On Linux

Go on the project folder:

```~$ cd /path/to/project/gaz_station_finder```

Then, you can activate your virtual environnement if you wish.

Install the requirements:

```~/path/to/project/gaz_station_finder$ pip3 install -r requirements.txt```

You can execute the search:

```~/path/to/project/gaz_station_finder$ python3 ./search --latitude=48.8319929 --longitude=2.3245488 --radius=5000 --date=2022-02-21 --gaz_type=SP98```

For the params definition see the Windows section.

To run the test:

 ```~/path/to/project/gaz_station_finder$ export PYTHONPATH=~/path/to/project/gaz_station_finder/gaz_station_finder/search```

 Then:

  ```~/path/to/project/gaz_station_finder$ python3 -m pytest tests```
