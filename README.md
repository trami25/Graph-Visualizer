# Graph-Visualizer <br>
SV 18/2021 Nikola Mitrović <br>
SV 27/2021 Vladislav Radović <br>
SV 58/2021 Aleksa Janjić <br>
SV 61/2021 Bojan Živanić

## Setup
Clone repo and then run `pip install -e ./graph_visualizer_api -e ./graph_visualizer_platform -e ./graph_visualizer_core`.

To start the django server, run `gv-manage runserver`.

## Project structure
The project consists of three main directories:
1. `graph_visualizer_api` - The API of the app containing interfaces and the graph model.
2. `graph_visualizer_platform` - This is the app platform that relies on the API and coordinates communication between the data source and visualizer.
3. `graph_visualizer_core` - This is the Django app that serves as a client and relies on the platform. It presents all the data being formed by the platform.

```mermaid
---
title: Architecture
---
classDiagram
    class Graph
    class Tree
    class VisualizerPlugin {
        <<interface>>
        + generate_template(graph: Graph) String
    }
    class DataSourcePlugin {
        <<interface>>
        + generate_graph() Graph
    }

    class Platform

    class DjangoApp
    
    VisualizerPlugin <-- Platform
    DataSourcePlugin <-- Platform
    Graph <-- Platform
    Tree <-- Platform
    Platform <-- DjangoApp
```

```mermaid
---
title: Graph and Tree
---
classDiagram
    class Graph
    class Node {
        - nodeId: int
        - data: Dictionary
    }
    class Edge
    class Tree {
        - directed: Boolean
    }
    class TreeNode
    
    Node <-- TreeNode : node
    TreeNode "*" <-- "1" TreeNode : - children
    TreeNode <-- Tree : - root
    Edge --> Node : - source
    Edge --> Node : - target
    Graph "1" --> "*" Node : - nodes
    Graph "1" --> "*" Edge : - edges
```

```mermaid
---
title: Platform
---
classDiagram
    class Facade
    class PluginManager {
        + getDataSourceByName(name: String) Plugin~DataSourcePlugin~
        + getVisualizerByName(name: String) Plugin~Visualizer~
    }
    class Plugin~T~ {
        - name: String
        - pluginType: Class~T~
        - instance: T
    }
    class WorkspaceManager {
        + spawn() void
        + kill(tag: String) void
    }
    class Workspace {
        - tag: String
        - activeDataSource: DataSourcePlugin
        - activeVisualizer: VisualizerPlugin
    }
    class GraphStore {
        - graph: Graph
        - subgraph: Graph
        - filters: Filter[]
        + addFilter(input: String)
        + removeFilter(filter: Filter)
    }
    class MainView {
        + update(graph: Graph)
    }
    class BirdView {
        + update(graph: Graph)
    }
    class TreeView {
        + update(graph: Graph)
    }
    class GraphListener {
        <<interface>>
        + update(graph: Graph)
    }
    
    PluginManager "1" -->  "*" Plugin : - dataSources
    PluginManager "1" -->  "*" Plugin : - visualizers
    WorkspaceManager "1" --> "*" Workspace : - workspaces
    Workspace --> GraphStore : - graphStore
    Workspace --> MainView
    Workspace --> BirdView
    Workspace --> TreeView
    MainView --|> GraphListener
    BirdView --|> GraphListener
    TreeView --|> GraphListener
    GraphStore "1" --> "*" GraphListener :  - listeners
```
