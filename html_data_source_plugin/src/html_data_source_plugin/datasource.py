from bs4 import BeautifulSoup
from graph_visualizer_api.datasource import DataSource
from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.node import Node
from graph_visualizer_api.model.edge import Edge
from html_data_source_plugin.provider import get_links, provide_for_url, get_metadata
from typing import Optional
from urllib.parse import urljoin


class HtmlDataSource(DataSource):
    """Scrapes and parses HTML to Graph.

    This is a plugin that implements the data source for the Graph Visualizer. It scrapes html pages and parses them
    to nodes. Each link to a node is parsed to an edge.

    Attributes:
        _base_url: Starting point for the scraper.
        _node_cap: Maximum number of nodes to be built.
        _next_node_id: Assigned to the next page.
        _graph: Parsed graph.
    """

    def __init__(self, base_url: str = 'http://www.scrapethissite.com', node_cap: int = 200):
        self._base_url = base_url
        self._node_cap = node_cap
        self._next_node_id = 1
        self._graph = Graph([], [])

    def _build_node(self, soup: BeautifulSoup, url: str) -> Node:
        """Builds the node from the soup object.

        :param soup: BeautifulSoup object.
        :param url: URL from which the soup object was created.
        :returns: Node object.
        """

        node_id = self._next_node_id
        self._next_node_id += 1

        node_data = {
            'url': url,
        }
        node_data.update(get_metadata(soup))

        print(f'Building node {node_id}...')
        return Node(node_id, node_data)

    def _process_node(self, node_url: str, previous_node: Optional[Node]) -> None:
        """Parses the page from the url.

        This is a recursive method and will be applied for each child of the current node i.e. the hyperlinks.

        :param node_url: The node URL.
        :param previous_node: Previous node.
        """

        if self._next_node_id > self._node_cap:
            return

        # Handle existing node
        nodes = self._graph.get_nodes_by_attributes(url=node_url)
        node = nodes[0] if len(nodes) > 0 else None
        if node is not None and previous_node is not None:
            edge = self._graph.get_edge(previous_node, node)
            if edge is None:
                self._graph.add_edge(Edge(previous_node, node, {}))
            return

        soup = provide_for_url(node_url)

        new_node = self._build_node(soup, node_url)
        self._graph.add_node(new_node)

        if previous_node is not None:
            self._graph.add_edge(Edge(previous_node, new_node, {}))  # TODO: add edge data

        links = get_links(soup)
        for link in links:
            path = ''
            if link and link.startswith('/'):
                path = urljoin(self._base_url, link)
            elif link and link.startswith('http'):
                path = link
            else:  # If no format is satisfied
                return

            self._process_node(path, new_node)

    def generate_graph(self) -> Graph:
        """Creates the graph.

        :return: Graph object.
        """
        self._process_node(self._base_url, None)

        return self._graph
