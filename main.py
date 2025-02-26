import requests 
import random
import os
from data_model import Base, Domains
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from models import Overview, HeadlineOverview, HeadlineSource
from pydantic import ValidationError
import webbrowser
from dotenv import load_dotenv

print("Setting up verification steps, please wait... \n")

load_dotenv()
apikey = os.getenv('apikey')

base_api_url = "https://newsapi.org/v2"

SQLALCHEMY_DATABASE_URL = "sqlite:///./domains.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# This binds our ORM class models
Base.metadata.create_all(bind=engine)
# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
# Current endpoint
endp = "/everything"
# 200 = ok, 400 = bad requests, 403 = forbidden, 422 = unprocessable entity (aka bad JSON), 500 = internal error, 502 = bad gateway, 503 = temporarily unavalible

sourceurls = []
sourceids = []

result = requests.get(f"https://newsapi.org/v2/top-headlines/sources?&apiKey={apikey}")
if result.status_code == 200:
    data = result.json()
    headlinesources = HeadlineOverview(**data)
    for source in headlinesources.sources:
        sourceurls.append(str(source.url))
        sourceids.append(source.id)


def menu():
    print("1. Make a search\n2. Check your feed\n3. Switch endpoints(search priority)\n4. Domains\n5. Exit\n")
    choice = input("Choose an option: ")

# Used to check if the supplied domains and keywords will provide a search, or that there are no errors.
def verify():
    print("test")
    # For now, not going to work on this. If time permits though, would like to make this a feature to cut down on some code.

# Takes the endpoint, and checks if it is /everything or /top-headlines. Then, if user permits, the enddpoint gets changed to it's counterpart.
def endpointswitch(endpoint):
    while True:
        if endpoint == "/everything":
            epchoice = input(f"Searches are currently set to search by /everything. Switch this to /top-headlines?(Y/N): ")
            if epchoice == "Y" or epchoice == "y":
                endpoint = "/top-headlines"
                os.system("cls")
                print("Switch successful! Returning to menu... \n")
                return endpoint
            elif epchoice == "N" or epchoice == "n":
                os.system("cls")
                print("Switch aborted, returning to menu... \n")
                break
            else:
                print("ERR: Not a valid choice. (ENDSW-DEC1-ERR) \n")
        elif endpoint == "/top-headlines":
            epchoice = input(f"Searches are currently set to search by /top-headlines. Switch this to /everything?(Y/N): ")
            if epchoice == "Y" or epchoice == "y":
                endpoint = "/top-headlines"
                os.system("cls")
                print("Switch successful! Returning to menu... \n")
                return endpoint
            elif epchoice == "N" or epchoice == "n":
                os.system("cls")
                print("Switch aborted, returning to menu... \n")
                break
            else:
                print("ERR: Not a valid choice. (ENDSW-DEC1-ERR) \n")



def search():
    # This is seperated into two sections, "/everything" and "/top-headlines". This is done because the endpoints process differently, like /top-headlines using sources and being able to search by countries

    os.system("cls")

    # /everything section
    if endp == "/everything":
        domlist = []
        # LOOK INTO TRIMMING
        keyword = input("Insert a keyphrase/keyword(use a comma seperated list for multiple): ").strip()
        if keyword != "":
            keyword = f"q={keyword}"
        domainselect = input("Would you like to search based on included domains, excluded domains or neither?(I/E/N): ")
        # If 'I', search is done based on domains user would like to see.
        if domainselect == "I" or domainselect == "i":
            searchdoms = session.execute(select(Domains).where(Domains.include == "include")).scalars()
            for value in searchdoms:
                domlist.append(value.domain)
            domstr = ",".join(domlist)
            domstr = f"&domains={domstr}"
        # If 'E', search is done based on domains user would like NOT to see.
        elif domainselect == "E" or domainselect == "e":
            searchdoms = session.execute(select(Domains).where(Domains.include == "exclude")).scalars()
            print(type(searchdoms))
            for value in searchdoms:
                domlist.append(value.domain)
            domstr = domstr = ",".join(domlist)
            domstr = f"&excludeDomains={domstr}"
        # If "N", search will not be based on domains
        elif domainselect == "N" or domainselect == "n":
            print("Search will not be based on domains, included or excluded.")
            domstr = ""
        # User is asked if they would like to sort by relevancy, popularity, date or neither.
        while True:
            sortchoice = input("Search by relevancy(r), popularity(p), date(d) or none(n)?: ")
            # 'sort' variable is what will be used to sort search.
            if sortchoice == "r" or sortchoice == "R":
                sort = "&sortBy=relevancy"
                break
            elif sortchoice == "p" or sortchoice == "P":
                sort = "&sortBy=popularity"
                break
            elif sortchoice == "d" or sortchoice == "D":
                sort = "&sortBy=publishedAt"
                break
            elif sortchoice == "n" or sortchoice == "N":
                sort = ""
                print("No sort priority will be applied.")
                break
            else:
                print("ERR: Not a valid choice. (SE-SORT-ERR)")
        result = requests.get(f"{base_api_url}{endp}?{keyword}{sort}{domstr}&pageSize=20&apiKey={apikey}")
        print(f"{base_api_url}{endp}{keyword}{sort}{domstr}&pageSize=20&apiKey={apikey}")
        if result.status_code == 200:
            data = result.json()
            articles = Overview(**data)
            if articles.message != None:
                print(articles.message)
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

    # /top-headlines section
    if endp == "/top-headlines":
        sourcelist = []
        keyword = input("Insert a keyphrase/keyword(use a comma seperated list for multiple): ")
        print("IMPORTANT NOTE: Some domains may not have a direct 'source', or may not translate well as sources. Search by sources with discretion.")
        while True:
            sourceselect = input("Search by saved sources(domains)?(Y/N): ")
            if sourceselect == "Y" or sourceselect == "y":
                searchdoms = session.execute(select(Domains).where(Domains.include == "include")).scalars()
                # COMARE FOUND DOMAINS TO FOUND SOURCES
                for value in searchdoms:
                    print(value.domain)
                    for source in sourceurls:
                        print(source)
                        if value.domain in source:
                            ind = sourceurls.index(source)
                            sourcelist.append(sourceids[ind])
                # FIND WAY TO CHECK VERIFY SOURCES, AND ADD THEM BASED ON THE MATCHING URLS
                sourcestr = ",".join(sourcelist)
                print(f"Sources found: {sourcestr}")
                break
            elif sourceselect == "N" or sourceselect == "n":
                print("Search will not be based on sources. ")
                break
            else:
                print("ERR: Not a valid choice. (SE-SOURCE-CHOICE-ERR)")
            

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
                        print("ERR: Not a valid choice. (DO-DEC1-ERR)")
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

search()