import yaml


class AnkimakerConfig(yaml.YAMLObject):
    yaml_tag = '!ankimakerconfig'
    header = None
    question_column = None
    answer_column = None
    separators = ','

    def __init__(self, header=None, answer_column=None, question_column=None):
        AnkimakerConfig.answer_column = answer_column
        AnkimakerConfig.question_column = question_column
        AnkimakerConfig.header = header
        AnkimakerConfig.AnkimakerConfig = AnkimakerConfig

    @staticmethod
    def loader(configuration_content):
        content = configuration_content['AnkimakerConfig']
        AnkimakerConfig.header = content.header
        AnkimakerConfig.question_column = content.question_column
        AnkimakerConfig.answer_column = content.answer_column
        AnkimakerConfig.separators = content.separators
