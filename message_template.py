from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text


class TextEditPrompt(Prompt):
    prompt_suffix = "> "


console = Console()


def create_message_template(settings):

    console.print("[bold green]Create your message template:[/]")
    console.print(
        "[italic]Include the placeholders [yellow]{my_first_name}[/] and [yellow]{their_first_name}[/].[/]"
    )
    console.print("[italic]Press Enter on an empty line to finish.[/]")
    console.print(
        "[italic]Example: Hi [yellow]{their_first_name}[/], I'm [yellow]{my_first_name}[/].[/]"
    )
    console.print("[italic cyan](Defaults to last saved template.)[/]")

    template_text = settings["messageTemplate"]
    while True:
        line = TextEditPrompt.ask("", default="", show_default=False)
        if line == "":
            break
        template_text += line + "\n"

    if not template_text:
        console.print("\n[bold red]Message template cannot be empty![/]\n")
        return create_message_template(settings)

    if (
        not "{my_first_name}" in template_text
        or not "{their_first_name}" in template_text
    ):
        console.print(
            "\n[bold red]Message template must include placeholders for first names![/]\n"
        )
        return create_message_template(settings)

    preview_text = Text(template_text)
    for placeholder in ["{my_first_name}", "{their_first_name}"]:
        preview_text.highlight_regex(placeholder, "yellow")
    console.print("\n[bold]Preview:[/]")
    console.print(preview_text)

    confirmed = Prompt.ask("Is this message template correct?", choices=["y", "n"])
    if confirmed == "y":
        return template_text
    else:
        return create_message_template(settings)
