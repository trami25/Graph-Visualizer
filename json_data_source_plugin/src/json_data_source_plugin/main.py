import time
from json_data_source_plugin.datasource import JsonDataSource
from json_data_source_plugin.provider import provide_json_data


def get_graph():
    json_data = provide_json_data("json_data_source_plugin\\data.json")
    json_data_source = JsonDataSource(json_data)

    graph = json_data_source.generate_graph()
    
    return graph

if __name__ == '__main__':
    
    json_data = provide_json_data("json_data_source_plugin\\data.json")
    json_data_source = JsonDataSource(json_data)

    start = time.time()
    graph = json_data_source.generate_graph()
    end = time.time()

    print(f'Number of nodes: {len(graph.nodes)}')
    print(f'Number of edges: {len(graph.edges)}')
    print(f'Time elapsed: {end - start}')
