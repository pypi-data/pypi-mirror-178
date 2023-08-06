# xpath-identifier
Given an html or similar input xpath-identifier returns the xpath of it's location in the input

## Usuage
from xpath_identifier import search_html
test_html = open("src/tests/fixtures/test_html.html").read()
xpaths = search_html(html_fixture, "Send them a gift tracking link")
print(xpaths)
>> ["/html/head/script[2]"]
