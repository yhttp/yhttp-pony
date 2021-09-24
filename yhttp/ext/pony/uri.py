import re


URI = re.compile(
    r'(?P<provider>.*)://(?P<user>.*):(?P<password>.*)@(?P<host>.*)/'
    r'(?P<database>.*)'
)


def parse(uri):
    match = URI.match(uri)
    if not match:
        raise ValueError(f'Invalid URI: {uri}')

    return {k: v for k, v in match.groupdict().items() if v}
