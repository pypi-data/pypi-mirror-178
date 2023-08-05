import uuid
import genanki


def create_deck(name, deck_id=None):
    if deck_id is None:
        deck_id = int(int(uuid.uuid4())//1e20)
    deck = genanki.Deck(
      deck_id,
      name
    )
    return deck


def save_deck(deck, destination, media_files=None):
    my_package = genanki.Package(deck)
    if media_files is not None:
        my_package.media_files = ['sound.mp3', 'images/image.jpg']
    my_package.write_to_file(destination)
