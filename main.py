from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from linkedin_api import Linkedin

from settings import DEFAULT_SETTINGS, load_settings, save_settings, update_settings
from linkedin import format_filters, search_people, load_urn_history, save_urn_history, connect_with_people

console = Console()
settings = DEFAULT_SETTINGS.copy()


def main():
    global settings

    console.print("[bold blue]LinkedIn Auto-Connect v1.0[/]")
    console.print("[italic blue]Marco Tan 2025[/]\n")
    console.print(
        "This script will attempt to search and connect with people on LinkedIn given user parameters."
    )
    console.print("Note the following [bold yellow]limitations[/]:")
    console.print(
        "\t1. LinkedIn will block your account if you send too many requests. The script will attempt to avoid this, but be warned."
    )
    console.print(
        "\t2. This script will occasionally require manual intervention for CAPTCHA challenges."
    )
    console.print("\t3. The script should be run on a home network to avoid IP blocks.")
    console.print(
        "\t4. The script can only search for people within your network and cannot connect with people outside your network."
    )
    console.print(
        "\t5. The script cannot handle Multi-Factor Authentication (MFA) challenges."
    )

    settings = load_settings()

    if settings == DEFAULT_SETTINGS:
        settings = update_settings(settings)
        save_settings(settings)

    while True:
        choices = {
            "1": "Update settings",
            "2": "Start connecting",
            "3": "Exit",
        }

        console.print("\n[bold blue]Main Menu[/]")
        for key, value in choices.items():
            console.print(f"[bold]{key}[/]. {value}")

        choice = Prompt.ask("Select an option", choices=choices.keys())

        if choice == "1":
            settings = update_settings(settings)
            save_settings(settings)
        elif choice == "2":
            num_connect = IntPrompt.ask(
                "Enter the number of connections to send", default=10
            )
            console.print("\n[bold blue]Connecting...[/]")

            history = load_urn_history()

            client = Linkedin(settings["username"], settings["password"])
            params = format_filters(settings)
            foundUrns = search_people(client, params, history, num_connect)

            successes = connect_with_people(client, foundUrns, history, settings)
            console.print(f"\n[bold green]{successes} connections sent![/]\n")
        elif choice == "3":
            console.print("\n[bold blue]Exiting...[/]")
            return


if __name__ == "__main__":
    main()
