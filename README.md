#  Star-tling Discoveries by 55-Cancri-Ae
## PM: Michelle Chen, Roster: Natalie Keiger, Ethan Cheung, & Thamidur Rahman
### Description
Our site will display the information from the dataset (https://exoplanetarchive.ipac.caltech.edu/index.html)  in an easily understandable table. The home page will guide the user, teaching them about what the data means. It will also teach them how to use the site. There is a explore page where you can choose what attributes to graph though either a line graph or scatter plot. Each planet will have its own page which will include all the data about it and a simulation of its orbit. There will be a separate page to explain what the terms mean.

### Install Guide:
1. Clone this repo:
```
git clone git@github.com:MichelleChen2331/p04-55-Cancri-Ae.git
```
2. Navigate into repo:
```
cd p04-55-Cancri-Ae
```

### Set up virtual environment:

``` python -m venv {{venv_path}} ```


### Activate virtual environment:

  - Linux/Mac:
    ``` source {{venv_path}}/bin/activate ```

  - Windows:
    ```{{venv_path}}\Scripts\activate ```


### Install requirements:

  ``` pip install -r requirements.txt ```



# Launch Codes:

### Activate virtual environment:

  - Linux/Mac:
    ``` source {{venv_path}}/bin/activate ```

  - Windows:
    ``` {{venv_path}}\Scripts\activate ```


### Navigate to app folder:

  ``` cd p04-55-Cancri-Ae/app ```

### Run \_\_init\_\_.py

  ``` python __init__.py ```


### Launch Codes:
```
python app/__init__.py
```

Live Website: http://167.172.242.87/home

### FEATURE SPOTLIGHT
* All the visualizations are interactive via plotly
* The Explore page allows you to pick what variables you want to compare and whether you want a scatter plot or line graph
* The definitions page lets you learn astronomy
### KNOWN BUGS/ISSUES
* The line plot doesn't average out the datas so its hard to intrepret
