from yhttp.extensions.pony import uri


def test_uriparse():
    assert uri.parse('postgres://foo:bar@baz/qux') == dict(
        user='foo',
        password='bar',
        host='baz',
        database='qux',
        provider='postgres',
    )

    assert uri.parse('postgres://foo:@/qux') == dict(
        user='foo',
        database='qux',
        provider='postgres',
    )

    assert uri.parse('postgres://:@foo/qux') == dict(
        host='foo',
        database='qux',
        provider='postgres',
    )

    assert uri.parse('postgres://:@/qux') == dict(
        database='qux',
        provider='postgres',
    )
