import click
import re
from ankimaker.commands import cli
from ankimaker.tasks import basic_pandas_to_anki


@cli.command('csv')
@click.argument('-i', '--input', 'input_file', type=click.Path(exists=True))
@click.argument('-o', '--output', 'output_file', type=click.Path(exists=False))
@click.option('-c', '--conf', 'config_file', default=None, type=click.STRING)
@click.option('-n', '--name', 'name', default=None, type=click.STRING)
def generate_anki(
        input_file,
        output_file,
        name,
        config_file,
):
    output_file = parse_output(output_file)
    if name is None:
        name = get_name_from_output(output_file)
    basic_pandas_to_anki(input_file, output_file, name, config_file)


def parse_output(filename):
    filetype = filename.split('.')[-1] if len(filename.split('.')) > 0 else None
    if filetype is None:
        return filename + '.apkg'
    elif filetype != 'apkg':
        filename.replace(filetype, 'apkg')
        return filename+filetype
    else:
        return filename


def get_name_from_output(filename):
    updated_file = filename.split('/')[-1] if len(filename.split('/')) > 0 else filename
    updated_file = re.sub(r'(.apkg)', '', updated_file)
    return updated_file
