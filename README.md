# CZ4034-Information-Retrieval-Assignment

## How to run the Covid Tweets Search Engine
1. **Create a virtual environment**
   1. open a terminal under the project folder
   2. run `pip install virtualenv` if `virtualenv` package is not already installed
   3. `virtualenv venv`
   4. `source venv/bin/activate`
2. **Install necessary libraries**
   1. `pip install -r requirements.txt`
3. **Pre-run settings**
   1. `cd backend/solr-8.11.1` from the project folder
   2. `bin/solr start`
4. **Run the app**
   1. `cd ui/UI/src` from the project folder
   2. `python manage.py migrate`
   3. `python manage.py runserver`
5. **Open the Search Engine in browser**
   1. open a browser, type `http://127.0.0.1:8000/` in the url box
6. **DONE!!**
