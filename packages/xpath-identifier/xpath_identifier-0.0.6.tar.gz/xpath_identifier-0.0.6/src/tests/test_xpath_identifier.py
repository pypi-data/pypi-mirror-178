import pytest
from xpath_identifier import search_email
from xpath_identifier import search_html

@pytest.fixture
def email_fixture():
    return open("src/tests/fixtures/test_email.eml").read()

@pytest.fixture
def html_fixture():
    return open("src/tests/fixtures/test_html.html").read()

def test_search_in_email(email_fixture):
    response = search_email(email_fixture, "9300120111409082698691")
    assert len(response) == 3
    assert response == [
        "/html/body/div/table/tr/td/table/tr/td/div[5]/div/table/tr/td/p[2]",
        "/html/body/div/table/tr/td/table/tr/td/div[5]/div/table/tr/td/p[2]/a",
        "/html/body/div/table/tr/td/table/tr/td/div[5]/div/table/tr/td/p[2]/a/span"
    ]
    assert search_email(email_fixture, "9405511202508597717093") == [
        "/html/body/div/table/tr/td/table/tr/td/div[6]/div/table/tr/td/p[2]",
        "/html/body/div/table/tr/td/table/tr/td/div[6]/div/table/tr/td/p[2]/a",
        "/html/body/div/table/tr/td/table/tr/td/div[6]/div/table/tr/td/p[2]/a/span"
    ]


def test_search_in_html(html_fixture):
    assert search_html(html_fixture, "Send them a gift tracking link") == [
        "/html/head/script[2]"
    ]
