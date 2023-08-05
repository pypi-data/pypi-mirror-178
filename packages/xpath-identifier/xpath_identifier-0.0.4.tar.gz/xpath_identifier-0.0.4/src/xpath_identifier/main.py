import re
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
    xpaths = []
    msg = Parser(policy=default_policy).parsestr(email)
    html_body = msg.get_body(preferencelist=("html")).get_content()
    return search_html(html_body, search_text)

def search_html(text: str, search_text: str) -> List[Optional[str]]:
    """
    Searches for xpath of input text
    @param text: text to search
    @return xpath:
    """
    xpaths = []
    soup = BeautifulSoup(text, "html.parser")
    soup_tag = _extract_soup_tag_from_soup(soup, search_text)
    if soup_tag:
        xpaths.append(_generate_xpath(soup_tag))
    return xpaths

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

def _extract_soup_tag_from_soup(html_soup: BeautifulSoup, text: str) -> Optional[Tag]:
    """
    Extracts a soup tag from the text.
    :param html_soup: The soup object.
    :param text: The text to search for.
    :return: The soup tag or None.
    """
    soup_tag = html_soup.find(lambda tag: text in tag.text, text=True)

    if not soup_tag:
        # soup tag was not found searching in text,
        # let's try to search for it in the tag attributes
        soup_tag = html_soup.find(
            lambda tag: any(text in x for x in tag.attrs.values())
        )

    return soup_tag

def validate_xpath(xpath:str, text: str, target_text: str) -> bool:
    """
    Validates xpath
    @param xpath: xpath to validate
    @param text: text to search in
    @param target_text: text to search for
    @return bool:
    """
    soup = BeautifulSoup(text, "html.parser")
    return bool(soup.select_one(xpath))

