import click

@click.group("cli")
def cli():
    pass


from ..commands.from_csv import generate_anki
