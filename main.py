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
    while True:
        doms = session.execute(select(Domains)).scalars()
        i = 1
        domlist = []
        dom = ""
        # Prints all saved domains, and stores them in domlist to be selected in the menu, based on their index in domlist.
        for value in doms:
            print(f"{i}. {value}")
            domlist.append(value.domain)
        while True:
            try:
                choice = input("Choose an option based on the number to update or delete(or type exit to quit): ")
                dom = domlist[int(choice)-1]
                break
            except IndexError:
                print("ERR: Not a valid option. (DO-IND-ERR)")
        print(f"What would you like to change on {dom}?: ")
        # Users can either change the domains name, change it's status, or delete it.
        print("1. Change domain name\n2. Change inclusion status\n3. Delete domain")
        choice = input("Choose an option: ")
        if choice == "1":
            newdom = input(f"Input a new name for {dom}: ")
            result = requests.get(f"{base_api_url}&domains={newdom}&apiKey={apikey}")
            # Checks if the API recognizes the domain.
            if result.status_code == 200:
                data = result.json()
                articles = Overview(**data)
                if articles.totalResults == 0:
                    print("ERR: This domain name is not valid. Please re-enter a new name. (DO-RENAME-ERR)")
                else:
                    # Changes the domain if user says 'y'
                    session.execute(update(Domains).where(Domains.domain == dom).values({Domains.domain: newdom}))
                    decision = f"ALERT: You are about to change {dom} to {newdom}. Do you confirm this choice?(Y/N): "
                    if decision == "Y" or decision == "y":
                        session.commit()
                        print("Update successful! \n")
                    elif decision == "N" or decision == "n":
                        print("Update aborted...")
                    else:
                        print("ERR: Not a valid choice. (DO-UPDEC-ERR)")
        elif choice == "2":
            # NEED TO GRAB INCLUSION STATUS TO DISPLAY
            print(f"{dom}'s status is currently set to ")
            print(f"What would you like to change {dom}'s inclusion status to?: ")
            print("1. Include \n2. Exclude\n3. Store\n4. Exit\n")
            incchoice = input("Choose an option: ")
            if incchoice == "1":
                session.execute(update(Domains).where(Domains.domain == dom).values({Domains.include: "include"}))
                session.commit()
                print("Status now set to include!")
            elif incchoice == "2":
                session.execute(update(Domains).where(Domains.domain == dom).values({Domains.include: "exclude"}))
                session.commit()
                print("Status now set to exclude!")
            elif incchoice == "3":
                session.execute(update(Domains).where(Domains.domain == dom).values({Domains.include: "stored"}))
                session.commit()
                print("Status now set to stored!")
        






domains()



