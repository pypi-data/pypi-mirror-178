from pathlib import Path
import yaml

from .configuration import AnkimakerConfig


def load_config_file(file_path: str):
    """
    Load yaml configuration file.
    :param file_path: Path to yaml file with configuration
    :return: Dict config
    """
    file_path = Path(file_path)
    assert file_path.exists()
    assert file_path.is_file()
    with open(file_path, 'r') as file:
        yaml.add_path_resolver('!ankimakerconfig', ['AnkimakerConfig'], dict)
        configuration = yaml.load(file.read(), Loader=yaml.Loader)
        AnkimakerConfig.loader(configuration)
