# Gaz station finder

This program helps you to find the cheapest gaz station around you and within a specified area.

To execute the search you need to download the xml data available [here](https://donnees.roulez-eco.fr/opendata/annee/2022) and put it inside the folder *ressources/oil_data*. The file needs to be called *PrixCarburants_annuel_2022.xml*.

The result will be a JSON file inside the folder *outputs* and called *results.json*.

If you want to use different names feel free to rename the names in the code as well.

## How to run

### On Windows

Open a Windows CMD and go to the project directory

```C:/ cd C:/path/to/project/gaz_station_finder```

Optionnal: Activate the Python virtual environnement. This step is not mandatory. **You need to have you own virtual environnement set up**.

```C:/path/to/project/gaz_station_finder> venv\Scripts\activate```

Install the requirements:

```(venv) C:/path/to/project/gaz_station_finder> pip install -r requirements.txt```

Launch the search:

 ```(venv) C:/path/to/project/gaz_station_finder> python3 ./search --latitude=48.8319929 --longitude=2.3245488 --radius=5000 --date=2022-02-21 --gaz_type=SP98```

 Execute the tests:

 Set the PYTHONPATH to the current directory

 ```(venv) C:/path/to/project/gaz_station_finder> set PYTHONPATH=C:/path/to/project/gaz_station_finder/search```

 Then you can run them:

 ```(venv) C:/path/to/project/gaz_station_finder> python3 -m pytest tests```

### On Linux

