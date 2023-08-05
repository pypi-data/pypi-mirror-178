from bs4 import BeautifulSoup
from bs4 import Tag
from typing import List, Optional
from email.parser import Parser
from email.policy import default as default_policy

def search_email(email: str, search_text: str) -> List[Optional[str]]:
    """
    Searches for xpath of input text
    @param text: text to search
    @return xpath:
    """
    html_body = _get_html_body_from_email(email)
    return search_html(html_body, search_text)

def search_html(html: str, search_text: str) -> List[Optional[str]]:
    """
    Searches for xpath of input text
    @param text: text to search
    @return xpath:
    """
    xpaths = []
    soup = _get_html_soup(html)
    soup_tags = _extract_soup_tags_from_soup(soup, search_text)
    if soup_tags:
        for soup_tag in soup_tags:
            # TODO: validate xpaths before appending
            # TODO: handle multiple child & parent xpaths
            xpaths.append(_generate_xpath(soup_tag))
    return xpaths

def _get_html_body_from_email(email: str) -> str:
    """
    Gets the html body from the email.
    :param email: The email.
    :return: The html body.
    """
    msg = Parser(policy=default_policy).parsestr(email)
    return msg.get_body(preferencelist=("html")).get_content()

def _get_html_soup(html: str) -> BeautifulSoup:
    """
    Gets the html soup.
    :param html: The html.
    :return: The soup object.
    """
    return BeautifulSoup(html, "html.parser")

def _generate_xpath(element: Tag) -> str:
    """
    Finds the xpath of the given element
    @param element: Soup element
    @return xpath: str
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if len(siblings) == 1
            else f"{child.name}[{next(i for i, s in enumerate(siblings, 1) if s is child)}]"
        )
        child = parent
    components.reverse()
    return f"/{'/'.join(components)}"

def _extract_soup_tags_from_soup(html_soup: BeautifulSoup, text: str) -> List[Optional[Tag]]:
    """
    Extracts all soup tags from the text.
    :param html_soup: The soup object.
    :param text: The text to search for.
    :return: The soup tag or None.
    """
    soup_text_tags = html_soup.find_all(lambda tag: text in tag.text, string=True) or []

    # let's try to search for it in the tag attributes
    soup_attr_tag = html_soup.find_all(
        lambda tag: any(text in x for x in tag.attrs.values())
    ) or []

    return soup_text_tags + soup_attr_tag
