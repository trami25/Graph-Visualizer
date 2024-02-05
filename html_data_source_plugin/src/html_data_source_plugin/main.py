from html_data_source_plugin.datasource import HtmlDataSource
import time

if __name__ == '__main__':
    html_data_source = HtmlDataSource()

    start = time.time()
    graph = html_data_source.generate_graph()
    end = time.time()

    print(graph)
    print(f'Number of nodes: {len(graph.nodes)}')
    print(f'Number of edges: {len(graph.edges)}')
    print(f'Time elapsed: {end - start}')
