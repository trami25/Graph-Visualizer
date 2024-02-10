from bs4 import BeautifulSoup
import requests


def provide_for_url(url: str) -> BeautifulSoup:
    """Returns soup object for given url.

    :param url: URL of the html document.
    :return: BeautifulSoup object.
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_links(soup: BeautifulSoup) -> list[str]:
    """Returns all hyperlink references.

    :param soup: BeautifulSoup object
    :returns: List of hyperlink references.
    """

    links = soup.find_all('a')

    return [link.get('href') for link in links]


def get_metadata(soup: BeautifulSoup) -> dict[str, str]:
    """Extracts metadata from soup object.

    :param soup: BeautifulSoup object.
    :return: Dictionary containing the metadata.
    """

    description = soup.find('meta', {'name': 'description'})
    charset = soup.meta
    title = soup.find('title')

    return {
        'title': title.string if title else 'No title',
        'description': description['content'] if description else 'No description',
        'charset': charset.get('charset') if charset else 'No charset',
    }
