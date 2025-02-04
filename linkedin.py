import re
import json
import os
from linkedin_api import Linkedin

def load_urn_history():
    history = []
    if os.path.exists("history.json"):
        with open("history.json", "r") as file:
            history = json.load(file)
    else:
        save_urn_history(history)
    return history

def save_urn_history(history):
    with open("history.json", "w") as file:
        json.dump(history, file)

def format_filters(settings):
    filters = ["(key:resultType,value:List(PEOPLE))"]
    if settings["searchParams"]["keywordSchool"]:
        filters.append(
            f"(key:schools,value:List({settings['searchParams']['keywordSchool']}))"
        )
    if settings["searchParams"]["keywordTitle"]:
        filters.append(
            f"(key:title,value:List({settings['searchParams']['keywordTitle']}))"
        )
    
    params = {"filters": "List({})".format(",".join(filters))}

    params["keywords"] = settings["searchParams"]["keywords"]

    return params

def search_people(client: Linkedin, params, history, limit):
    people_list = []
    index = 0
    while True:
        response = client.search(params, limit=25, offset=index)
        for person in response:
            entityUrn = person["entityUrn"]
            pattern = r"urn:li:fsd_profile:([^,]+)"
            match = re.search(pattern, entityUrn)

            urn = match.group(1) if match else None

            titleAccessibilityText = person["title"]["accessibilityText"]
            pattern = r"View\s+(.+?)['’‘]s\s+profile"
            match = re.search(pattern, titleAccessibilityText)

            name = match.group(1) if match else None

            if urn and name and urn not in [x[0] for x in history]:
                people_list.append((urn, name))
            
            if len(people_list) >= limit:
                return people_list
        
        index += 25
