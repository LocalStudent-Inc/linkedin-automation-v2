import re
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def get_email(settings):
    email = Prompt.ask(
        "Enter your LinkedIn email address",
        default=settings["username"],
        show_default=settings["username"] != "",
    )
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        console.print("\n[bold red]Invalid email address![/]\n")
        return get_email(settings)
    return email

def get_keywords(settings):
    keywords = Prompt.ask(
        "Enter keywords to search for (separate with spaces)",
        default=settings["searchParams"]["keywords"],
        show_default=settings["searchParams"]["keywords"] != "",
    )
    if keywords == "":
        console.print("\n[bold red]Keywords cannot be empty![/]\n")
        return get_keywords(settings)
    return keywords