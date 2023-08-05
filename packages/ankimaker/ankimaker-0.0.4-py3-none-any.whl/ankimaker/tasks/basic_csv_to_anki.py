import genanki
import pandas as pd

from ankimaker.config import Config
from ankimaker import generator, config


def create_model():
    my_model = genanki.Model(
      1607392319,
      'Simple Model',
      fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
      ],
      templates=[
        {
          'name': 'Card 1',
          'qfmt': '<div style="text-align: center;">{{Question}}</div>',
          'afmt': '{{FrontSide}}<hr id="answer"><div style="text-align: center;">{{Answer}}</div>',
        },
      ])
    return my_model


def create_note(model, fields):
    note = genanki.Note(
        model=model,
        fields=fields
    )
    return note


def load_csv(path):
    df = pd.read_csv(path, header=Config.header, sep=Config.separators)
    df_columns_are_unnamed = all(map(lambda x: str(x).isnumeric(), df.columns))
    if df_columns_are_unnamed:
        Config.answer_column = int(Config.answer_column)
        Config.question_column = int(Config.question_column)
    return df


def add_df_to_deck(df: pd.DataFrame, deck: genanki.Deck):
    model = create_model()

    for entry in df.to_dict('records'):
        question = entry[Config.question_column]
        answer = entry[Config.answer_column]
        content_fields = (question, answer)
        note = create_note(model, fields=content_fields)
        deck.add_note(note)
    return deck


def handle_config(config_file_path):
    if config_file_path is None:
        Config.header = None
        Config.question_column = 0
        Config.answer_column = 1
    else:
        config.load_config_file(config_file_path)


def basic_pandas_to_anki(csv_path, output_path, name, config_file_path):
    handle_config(config_file_path)
    df = load_csv(csv_path)
    deck = generator.deck.create_deck(name)
    add_df_to_deck(df, deck)
    generator.deck.save_deck(deck, output_path)
