from . import uri


def initialize(db, settings):
    url = uri.parse(settings.url)
    db.bind(**url)
    db.generate_mapping(create_tables=True)


def deinitialize(db):
    db.disconnect()
    if db.provider is not None:
        db.provider.disconnect()
        db.provider = None

    db.schema = None
