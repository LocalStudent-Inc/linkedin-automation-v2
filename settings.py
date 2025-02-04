import json
import os
import datetime

from rich.console import Console
from rich.prompt import Prompt, IntPrompt

from input_validation import get_email, get_keywords
from message_template import create_message_template

DEFAULT_SETTINGS = {
    "username": "",
    "password": "",
    "myFirstName": "",
    "searchParams": {
        "keywords": "",
        "keywordSchool": "",
        "keywordTitle": "",
    },
    "weeklyLimit": 100,
    "currentWeekCount": 0,
    "lastUpdated": "",
    "messageTemplate": "",
}

console = Console()
def load_settings():
    settings = {}

    if os.path.exists("settings.json"):
        with open("settings.json", "r") as file:
            settings = json.load(file)

            if not all(key in settings for key in DEFAULT_SETTINGS.keys()):
                console.print("\n[bold red]Invalid settings file![/]")
                console.print(
                    "[bold red]Settings will be reset to default values.[/]\n"
                )
                settings = DEFAULT_SETTINGS.copy()
            else:
                console.print("\n[bold green]Settings loaded successfully![/]\n")

    else:
        console.print("\n[bold red]No settings file found![/]\n")
        settings = DEFAULT_SETTINGS.copy()
    
    return settings

def save_settings(settings):
    with open("settings.json", "w") as file:
        json.dump(settings, file)
        console.print("\n[bold green]Settings saved successfully![/]\n")

def update_settings(settings):
    settings = settings.copy()

    console.print("[bold blue]Update Settings[/]\n")

    settings["myFirstName"] = Prompt.ask(
        "Enter your first name",
        default=settings["myFirstName"],
        show_default=settings["myFirstName"] != "",
    )

    settings["username"] = get_email(settings)

    settings["password"] = Prompt.ask(
        f"Enter your LinkedIn password{settings["password"] and ' [bold cyan](default last saved)[/]'}",
        password=True,
        default=settings["password"],
        show_default=False,
    )

    settings["searchParams"]["keywords"] = get_keywords(settings)

    settings["searchParams"]["keywordSchool"] = Prompt.ask(
        "Enter a school to filter by (optional)",
        default=settings["searchParams"]["keywordSchool"],
        show_default=settings["searchParams"]["keywordSchool"] != "",
    )

    settings["searchParams"]["keywordTitle"] = Prompt.ask(
        "Enter a title to filter by (optional)",
        default=settings["searchParams"]["keywordTitle"],
        show_default=settings["searchParams"]["keywordTitle"] != "",
    )

    settings["weeklyLimit"] = IntPrompt.ask(
        "Enter the weekly connection limit", default=settings["weeklyLimit"]
    )

    settings["messageTemplate"] = create_message_template(settings)

    settings["lastUpdated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return settings
