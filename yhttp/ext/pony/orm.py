from yhttp.ext.dbmanager import DatabaseURI


def initialize(db, url, create_objects=False):
    url = DatabaseURI.loads(url)
    db.bind(**url.todict())
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
