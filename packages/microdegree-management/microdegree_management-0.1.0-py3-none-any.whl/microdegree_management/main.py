from typing import Optional, Union, Literal
from pathlib import Path
from pydantic import Extra
from pydantic_yaml import YamlModel
import tempfile
import click

# unfortunately there is no type info ATM
import graphviz  # type: ignore
import yaml


class URL(YamlModel):
    url: str
    description: str


class Assignment(YamlModel):
    description: str
    path: Path
    attachments: Optional[list[Path]]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "description": "Oefening for lus",
                    "path": "oefeningen/TypeScript/oefening-for-lus.md",
                    "attachments": ["oefeningen/TypeScript/screenshot-for-lus.png"],
                }
            ]
        }


class Job(YamlModel, extra=Extra.forbid):
    kind: Literal["text"] | Literal["video"] | Literal["proof"] | Literal["assignments"]
    assignee: str
    status: Literal["planned"] | Literal["drafted"] | Literal["reviewable"] | Literal[
        "accepted"
    ] | Literal["needs_update"]
    notes: Optional[str]


class Node(YamlModel, extra=Extra.forbid):
    id: str
    title: Optional[str]
    assignments: Optional[list[Assignment]]
    urls: Optional[list[URL]]
    jobs: Optional[list[Job]]


class NodePlaceholder(YamlModel, extra=Extra.forbid):
    cluster: str
    id: str


class Edge(YamlModel, extra=Extra.forbid):
    start_id: str
    end_id: str


class Cluster(YamlModel, extra=Extra.forbid):
    namespace_prefix: str
    nodes: list[Node]
    edges: list[Edge]


class Module(YamlModel, extra=Extra.forbid):
    clusters: list[Cluster]


@click.group()
def cli() -> None:
    pass


@click.command()
@click.argument("paths", type=click.Path(exists=True), nargs=-1)
def visualize_module(paths) -> None:
    module = Module(clusters=[])
    for path in paths:
        module.clusters.append(Cluster.parse_file(path))
    dot = graphviz.Digraph()
    for cluster in module.clusters:
        nodes: list[Node] = cluster.nodes
        for node in nodes:
            dot.node(f"{cluster.namespace_prefix}__{node.id}", node.title or node.id)
        edges: list[Edge] = cluster.edges
        for edge in edges:
            start_id = edge.start_id
            end_id = edge.end_id
            if "__" not in start_id:
                start_id = f"{cluster.namespace_prefix}__{start_id}"
            if "__" not in end_id:
                end_id = f"{cluster.namespace_prefix}__{end_id}"
            dot.edge(start_id, end_id)
    dot.render("module.gv", directory=tempfile.gettempdir(), cleanup=True, view=True)


cli.add_command(visualize_module)


@click.command()
@click.argument("path", type=click.Path(exists=True))
def visualize_cluster(path) -> None:
    cluster: Cluster = Cluster.parse_file(path)
    dot = graphviz.Digraph()
    nodes: list[Node] = cluster.nodes
    for node in nodes:
        dot.node(f"{cluster.namespace_prefix}__{node.id}", node.title or node.id)
    edges: list[Edge] = cluster.edges
    for edge in edges:
        start_id = edge.start_id
        end_id = edge.end_id
        if "__" not in start_id:
            start_id = f"{cluster.namespace_prefix}__{start_id}"
        if "__" not in end_id:
            end_id = f"{cluster.namespace_prefix}__{end_id}"
        dot.edge(start_id, end_id)
    dot.render("cluster.gv", directory=tempfile.gettempdir(), cleanup=True, view=True)


cli.add_command(visualize_cluster)


def writeschema() -> None:
    with open("tests/testschema.json", mode="w") as fh:
        fh.write(Cluster.schema_json(indent=2))


def check_redundancy(module: Module) -> Optional[str]:
    raise NotImplementedError("Cannot check for redundancy yet.")


@click.command()
@click.argument("paths", type=click.Path(exists=True), nargs=-1)
def validate_module(paths) -> None:
    module = Module(clusters=[])
    for path in paths:
        module.clusters.append(Cluster.parse_file(path))
    qualified_names: set[str] = set()
    # TODO
    # additional checks
    # placeholder nodes should only have one __
    # same goes for edges
    # and all edges must refer to VALID namespaces
    # could also prohibit namespacing end nodes!
    for cluster in module.clusters:
        for node in cluster.nodes:
            if "__" in node.id:
                raise ValueError("Regular node ID should not mention namespace.")
            qualified_names.add(f"{cluster.namespace_prefix}__{node.id}")
    for cluster in module.clusters:
        cluster_node_ids = [node.id for node in cluster.nodes]
        for edge in cluster.edges:
            if (
                edge.start_id not in cluster_node_ids
                and edge.start_id not in qualified_names
            ):
                raise ValueError(
                    f"Edge {edge.start_id} -> {edge.end_id} contains unknown start node"
                )
            if (
                edge.end_id not in cluster_node_ids
                and edge.end_id not in qualified_names
            ):
                raise ValueError(
                    f"Edge {edge.start_id} -> {edge.end_id} contains unknown end node"
                )


cli.add_command(validate_module)


# TODO: add commands to show dependencies / assignees within module / within cluster

if __name__ == "__main__":
    cli()
