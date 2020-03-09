# JDUAR NVIDIA - Smart CRM Backend
Smart CRM (Customer Relationship Management) is a progressive web app (PWA) which can ease customer in membership registration. Smart CRM implements face recognition and face identification to identify if a customer is already registered as member or not.

## Staging Pipeline Status
[![Pipeline](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/jduar-nvidia-smart-crm/badges/staging/pipeline.svg)](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/jduar-nvidia-smart-crm/commits/staging) 
[![coverage report](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/jduar-nvidia-smart-crm/badges/staging/coverage.svg)](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/jduar-nvidia-smart-crm/commits/staging)

## Projects URL
Staging : https://ppl-smartcrm-backend.herokuapp.com

Production : https://smart-crm-backend.herokuapp.com


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
* Install python 3  [here](https://www.python.org/downloads/) 
* Install git [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Installing

A step by step series to get a development env running in your local PC

* Init git using :

(you must install git first in prerequisites)
```
git init
```

* Clone this repository using http :
```
git clone https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/jduar-nvidia-smart-crm.git
```

* or Clone this repository using ssh :
```
git clone git@gitlab.cs.ui.ac.id:ppl-fasilkom-ui/2020/jduar-nvidia-smart-crm.git
```

* Open our directory using :
```
cd jduar-nvidia-smart-crm
```

* Install all library depedencies using :
```
pip install -r requirements.txt
```

## Running App


Run this app using :
```
python manage.py runserver
```

Open your favourite web browser and open app's localhost (usually using 8000 as its port)

If you want to run this app with its UI, you must setting up and run our Fronted. You can access out Frontend repository [here](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/jduar-nvdia-smart-crm-frontend).


## Running Test
Run unittest using :
```
python manage.py test
```

Run code style test (we're using pylint) using :

```
pylint --output-format=text crossroads/tests.py crossroads/views.py crossroads/validator.py enhancer/compressor.py enhancer/image_processor.py enhancer/tests.py
```

## Apps
List of our apps, we use unconventional naming.

### Hello
Simple hello world app.

### Crossroads
Main app to control program flow between frontend API and dummy of XQ's API.

### Enhancer
App to make image enhancements. Will include image compression and enhancing of images received from frontend.

### Connor (TBD)
Face recognition app to be developed.

## Authors

* **Alya Zahra** (1706039906)
* **Gusti Ngurah Yama Adi Putra** (1706979253)
* **Julia Ningrum** (1706979322)
* **Rafif Taris** (1706979436)
* **Raihansyah Attallah Andrian** (1706040196)

Code with :heart: for PROYEK PERANGKAT LUNAK course of University of Indonesia Faculty of Computer Science.