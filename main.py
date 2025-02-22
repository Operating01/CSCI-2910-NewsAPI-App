import requests 
import random
import os
from data_model import Base, Domains
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from models import Overview
from pydantic import ValidationError
import webbrowser
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv('apikey')

base_api_url = "https://newsapi.org/v2/everything?q="

SQLALCHEMY_DATABASE_URL = "sqlite:///./domains.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# This binds our ORM class models
Base.metadata.create_all(bind=engine)
# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# 200 = ok, 400 = bad requests, 403 = forbidden, 422 = unprocessable entity (aka bad JSON), 500 = internal error, 502 = bad gateway, 503 = temporarily unavalible


def menu():
    print("1. Make a search\n2. Check your feed\n3. Switch endpoints(search priority)\n4. Domains\n5. Exit\n")
    choice = input("Choose an option: ")

def search():
    keyword = input("Insert a keyphrase/keyword(use a comma seperated list for multiple): ")
    domains = input("Would you like to search based on included domains, excluded domains or neither?(I/E/N): ")
    result = requests.get(f"{base_api_url}{keyword}&domains=&pageSize=20&{apikey}")
    if result.status_code == 200:
        data = result.json()
        articles = Overview(**data)
        random.shuffle(articles.articles)
        i = 1
        heldarticles = []
        for value in articles.articles:
            print(f"{i}. {value.__repr__()}")
            heldarticles.append(value.url)
            i += 1
            #if i == 6:
            # visit = input("Would you like to visit any of the displayed articles?: ")
            # visit = int(visit) - 1
            # webbrowser.open(str(heldarticles[visit]))
            # i = 1

def domains():
    #session.execute(insert(Domains).values(domain = "verge.com", include = "include"))
   # session.commit()
    doms = session.execute(select(Domains)).scalars()
    i = 1
    domlist = []
    for value in doms:
        print(f"{i}. {value}")
        domlist.append(value.domain)
    try:
        choice = input("Choose an option based on the number to update or delete(or type exit to quit): ")
        option = domlist[int(choice)]
    except IndexError:
        print("ERR: Not a valid option. (DO-IND-ERR)")
domains()



