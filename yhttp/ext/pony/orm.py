from . import uri


def initialize(db, url, create_objects=False):
    url = uri.parse(url)
    db.bind(**url)
    db.generate_mapping(
        check_tables=create_objects,
        create_tables=create_objects
    )


def deinitialize(db):
    db.disconnect()
    if db.provider is not None:
        db.provider.disconnect()
        db.provider = None

    db.schema = None
