from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pytest import raises

from pando.http.request import Headers
import pando.body_parsers as parsers
from pando.exceptions import MalformedBody, UnknownBodyType


FORMDATA = object()
WWWFORM = object()

def make_body(raw, headers=None, content_type=WWWFORM):
    if not isinstance(raw, bytes):
        raw = raw.encode('ascii')
    if headers is None:
        defaults = { FORMDATA: b"multipart/form-data; boundary=AaB03x",
                     WWWFORM: b"application/x-www-form-urlencoded" }
        headers = {b"Content-Type": defaults.get(content_type, content_type)}
    if not b'content-length' in headers:
        headers[b'Content-length'] = str(len(raw)).encode('ascii')
    body_parsers = {
            "application/json": parsers.jsondata,
            "application/x-www-form-urlencoded": parsers.formdata,
            "multipart/form-data": parsers.formdata
    }
    headers[b'Host'] = b'Blah'
    return parsers.parse_body(raw, Headers(headers), body_parsers)


def test_body_is_unparsed_for_empty_content_type():
    raw = "cheese=yes"
    raises(UnknownBodyType, make_body, raw, headers={})

def test_body_barely_works():
    body = make_body("cheese=yes")
    actual = body['cheese']
    assert actual == "yes"


UPLOAD = '\r\n'.join("""\
--AaB03x
Content-Disposition: form-data; name="submit-name"

Larry
--AaB03x
Content-Disposition: form-data; name="files"; filename="file1.txt"
Content-Type: text/plain

... contents of file1.txt ...
--AaB03x--
""".splitlines())

def test_body_barely_works_for_form_data():
    body = make_body(UPLOAD, content_type=FORMDATA)
    actual = body['files'].filename
    assert actual == "file1.txt"

def test_simple_values_are_simple():
    body = make_body(UPLOAD, content_type=FORMDATA)
    actual = body['submit-name']
    assert actual == "Larry"

def test_multiple_values_are_multiple():
    body = make_body("cheese=yes&cheese=burger")
    assert body.all('cheese') == ["yes", "burger"]

def test_params_doesnt_break_www_form():
    body = make_body("statement=foo"
                    , content_type=b"application/x-www-form-urlencoded; charset=UTF-8; cheese=yummy"
                     )
    actual = body['statement']
    assert actual == "foo"

def test_malformed_body_jsondata():
    with raises(MalformedBody):
        make_body("foo", content_type=b"application/json")

def test_malformed_body_formdata():
    with raises(MalformedBody):
        make_body("", content_type=b"multipart/form-data; boundary=\0")
