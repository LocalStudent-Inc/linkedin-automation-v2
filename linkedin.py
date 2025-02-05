import re
import json
import os
import random
import time
import datetime
from linkedin_api import Linkedin
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.progress import track, Progress

from settings import save_settings

console = Console()

def load_urn_history():
    history = []
    if os.path.exists("history.json"):
        with open("history.json", "r") as file:
            console.print("\n[bold green]History loaded successfully![/]\n")
            history = json.load(file)
    else:
        console.print("\n[bold red]No history file found![/] Creating new one...\n")
        save_urn_history(history)
    return history

def save_urn_history(history):
    with open("history.json", "w") as file:
        console.print("\n[bold green]History saved successfully![/]\n")
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
    console.print("\n[bold blue]Searching for people...[/]\n")

    people_list = []
    index = 0

    with Progress() as progress:
        task = progress.add_task("[cyan]Searching...", total=limit)

        while True:
            response = client.search(params, limit=25, offset=index)
            for person in response:
                entityUrn = person["entityUrn"]
                pattern = r"urn:li:fsd_profile:([^,]+)"
                match = re.search(pattern, entityUrn)

                urn = match.group(1) if match else None

                titleAccessibilityText = person["title"]["accessibilityText"]
                pattern = r"View\s+(.+?)['’‘]s\s+profile"
                match = re.search(pattern, titleAccessibilityText or "")

                name = match.group(1) if match else None

                if urn and name and urn not in [x[0] for x in history]:
                    progress.update(task, advance=1)
                    people_list.append((urn, name))
                
                if len(people_list) >= limit:
                    return people_list
            
            index += 25

def connect_with_people(client: Linkedin, found_urns, history, settings):
    weeklyLimit = settings["weeklyLimit"]
    messageTemplate = settings["messageTemplate"]
    myFirstName = settings["myFirstName"]

    table = Table(title="Connection List")
    table.add_column("Name")
    table.add_column("Status")
    table.add_column("Time Connected")

    successful_connections = 0

    with Live(table, console=console, screen=True, refresh_per_second=4) as live:
        for urn, name in track(found_urns, description="Connecting..."):
            if settings["currentWeekCount"] >= weeklyLimit:
                console.print("\n[bold red]Weekly limit reached![/]\n")
                return
            
            first_name = re.match(r"^([\w\-]+)", name, re.UNICODE).group(1)
            message = messageTemplate.format(my_first_name=myFirstName, their_first_name=first_name)

            # client would be connected here
            # res = client.add_connection(profile_urn=urn, message=message)
            console.print(f"Message sent to {first_name} with message: {message}!")
            res = True # dummy response

            if res:
                history.append([urn, name])
                settings["currentWeekCount"] += 1
                successful_connections += 1
                status = "[bold green]Connected[/]"
            else:
                status = "[bold red]Failed[/]"
                console.print("\n[bold red]Failed to connect! An unknown error occurred.[/]\n")

            table.add_row(name, status, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            delay = random.randint(15, 60)
            console.print(f"Waiting {delay} seconds before connecting with the next person...")
            time.sleep(delay)
    
    save_urn_history(history)
    save_settings(settings)

    return successful_connections
