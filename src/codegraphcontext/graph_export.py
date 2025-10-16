"""
graph_export.py
----------------
Utility for exporting the internal code graph into a Graphviz DOT (.dot) file.

This script assumes there is a graph object or manager with methods to list
nodes and edges. You can integrate it with your existing graph backend easily.

Usage (CLI):
    python3 -m codegraphcontext.graph_export --output graph.dot
    python3 -m codegraphcontext.graph_export --output graph.dot --limit 100
"""

import argparse
import sys
from typing import List, Optional, Any


class SimpleGraph:
    """
    Mock graph structure for demonstration.
    Replace this with your actual graph manager (e.g., Neo4j, NetworkX, etc.).
    """
    def __init__(self):
        # Example sample graph
        self.nodes = [
            {"id": "FuncA", "label": "FuncA", "type": "function"},
            {"id": "FuncB", "label": "FuncB", "type": "function"},
            {"id": "ClassX", "label": "ClassX", "type": "class"},
        ]
        self.edges = [
            {"source": "FuncA", "target": "FuncB", "label": "calls"},
            {"source": "ClassX", "target": "FuncA", "label": "contains"},
        ]

    def get_nodes(self) -> List[Any]:
        return self.nodes

    def get_edges(self) -> List[Any]:
        return self.edges


def export_to_dot(
    graph: SimpleGraph,
    output_path: str,
    limit: Optional[int] = None,
    node_types: Optional[List[str]] = None,
    edge_labels: Optional[List[str]] = None,
) -> None:
    """
    Export graph data to Graphviz DOT format.
    """
    nodes = graph.get_nodes()
    edges = graph.get_edges()

    if node_types:
        nodes = [n for n in nodes if n["type"] in node_types]
        valid_ids = {n["id"] for n in nodes}
    else:
        valid_ids = {n["id"] for n in nodes}

    if edge_labels:
        edges = [e for e in edges if e["label"] in edge_labels]
    edges = [e for e in edges if e["source"] in valid_ids and e["target"] in valid_ids]

    if limit:
        nodes = nodes[:limit]
        valid_ids = {n["id"] for n in nodes}
        edges = [e for e in edges if e["source"] in valid_ids and e["target"] in valid_ids]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("digraph CodeGraph {\n")
        for n in nodes:
            label = f'{n["label"]}\\n({n["type"]})'
            f.write(f'  "{n["id"]}" [label="{label}"];\n')
        for e in edges:
            f.write(f'  "{e["source"]}" -> "{e["target"]}" [label="{e["label"]}"];\n')
        f.write("}\n")

    print(f"[✓] Graph exported successfully to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Export internal code graph to Graphviz DOT format."
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output file path for the .dot file",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        help="Limit number of nodes to export",
    )
    parser.add_argument(
        "--node-types",
        nargs="*",
        help="Filter by node types (e.g. function class variable)",
    )
    parser.add_argument(
        "--edge-labels",
        nargs="*",
        help="Filter by edge labels (e.g. calls inherits contains)",
    )

    args = parser.parse_args()

    g = SimpleGraph()  # replace with your graph manager
    export_to_dot(
        g,
        output_path=args.output,
        limit=args.limit,
        node_types=args.node_types,
        edge_labels=args.edge_labels,
    )


if __name__ == "__main__":
    main()
