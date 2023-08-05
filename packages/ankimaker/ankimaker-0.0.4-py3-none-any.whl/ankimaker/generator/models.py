import genanki as anki

simple_flashcard = anki.Model(
    16073923194617823,
    name='simple_flashcard',
    fields=[
        {'name': 'word'},
        {'name': 'meaning'}
    ],
    templates=[
        {
            'name': 'geneticname',
            'qfmt': '{{word}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{meaning}}'
        }
    ]
)
