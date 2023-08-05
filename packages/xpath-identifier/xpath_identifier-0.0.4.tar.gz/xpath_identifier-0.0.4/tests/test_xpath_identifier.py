import pytest
from xpath_identifier import search_email
from xpath_identifier import search_html

@pytest.fixture
def email_fixture():
    return open("tests/fixtures/test_email.eml").read()

@pytest.fixture
def html_fixture():
    return open("tests/fixtures/test_html.html").read()

def test_search_in_email(email_fixture):
    assert search_email(email_fixture, "9300120111409082698691") == [
        "/html/body/div/table/tr/td/table/tr/td/div[5]/div/table/tr/td/p[2]"
    ]
    assert search_email(email_fixture, "9405511202508597717093") == [
        "/html/body/div/table/tr/td/table/tr/td/div[6]/div/table/tr/td/p[2]"
    ]
