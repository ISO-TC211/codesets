#!/usr/bin/env python3
"""Print a SKOS concept hierarchy from a vocabulary file or URL."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS


INDENT = "  "


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a SKOS Concept hierarchy using skos:broader or skos:narrower relations."
    )
    parser.add_argument(
        "vocabulary",
        help="Path or URL for a SKOS vocabulary, such as resources/codesets/RegisterItemStatus.ttl",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="rdf_format",
        help="RDF input format. If omitted, rdflib guesses from the file extension.",
    )
    parser.add_argument(
        "-r",
        "--relation",
        choices=("auto", "broader", "narrower", "both"),
        default="auto",
        help="SKOS hierarchy relation to use. 'auto' prefers broader and falls back to narrower.",
    )
    parser.add_argument(
        "-s",
        "--scheme",
        help="Only print concepts in this ConceptScheme IRI.",
    )
    parser.add_argument(
        "-l",
        "--lang",
        default="en",
        help="Preferred language for skos:prefLabel values. Defaults to 'en'.",
    )
    parser.add_argument(
        "--show-iri",
        action="store_true",
        help="Print each concept IRI after its label.",
    )
    return parser.parse_args()


def load_graph(source: str, rdf_format: str | None) -> Graph:
    graph = Graph()
    graph.parse(source, format=rdf_format)
    return graph


def concepts_for_scheme(graph: Graph, scheme: URIRef | None) -> set[URIRef]:
    if scheme is None:
        concepts = set(graph.subjects(RDF.type, SKOS.Concept))
        concepts.update(s for s, _ in graph.subject_objects(SKOS.broader) if isinstance(s, URIRef))
        concepts.update(o for _, o in graph.subject_objects(SKOS.broader) if isinstance(o, URIRef))
        concepts.update(s for s, _ in graph.subject_objects(SKOS.narrower) if isinstance(s, URIRef))
        concepts.update(o for _, o in graph.subject_objects(SKOS.narrower) if isinstance(o, URIRef))
        concepts.update(o for _, o in graph.subject_objects(SKOS.hasTopConcept) if isinstance(o, URIRef))
        concepts.update(s for s, _ in graph.subject_objects(SKOS.topConceptOf) if isinstance(s, URIRef))
        return concepts

    concepts = set(graph.subjects(SKOS.inScheme, scheme))
    concepts.update(graph.subjects(SKOS.topConceptOf, scheme))
    concepts.update(graph.objects(scheme, SKOS.hasTopConcept))
    return {concept for concept in concepts if isinstance(concept, URIRef)}


def add_broader_edges(
    graph: Graph, concepts: set[URIRef], children: dict[URIRef, set[URIRef]]
) -> int:
    count = 0
    for child, parent in graph.subject_objects(SKOS.broader):
        if isinstance(child, URIRef) and isinstance(parent, URIRef) and child in concepts and parent in concepts:
            children[parent].add(child)
            count += 1
    return count


def add_narrower_edges(
    graph: Graph, concepts: set[URIRef], children: dict[URIRef, set[URIRef]]
) -> int:
    count = 0
    for parent, child in graph.subject_objects(SKOS.narrower):
        if isinstance(parent, URIRef) and isinstance(child, URIRef) and parent in concepts and child in concepts:
            children[parent].add(child)
            count += 1
    return count


def build_children(graph: Graph, concepts: set[URIRef], relation: str) -> dict[URIRef, set[URIRef]]:
    children: dict[URIRef, set[URIRef]] = defaultdict(set)

    if relation in ("broader", "both"):
        add_broader_edges(graph, concepts, children)
    elif relation == "narrower":
        add_narrower_edges(graph, concepts, children)
    else:
        broader_count = add_broader_edges(graph, concepts, children)
        if broader_count == 0:
            add_narrower_edges(graph, concepts, children)

    if relation == "both":
        add_narrower_edges(graph, concepts, children)

    return children


def top_concepts(graph: Graph, concepts: set[URIRef], scheme: URIRef | None) -> set[URIRef]:
    if scheme is not None:
        explicit_roots = set(graph.objects(scheme, SKOS.hasTopConcept))
        explicit_roots.update(graph.subjects(SKOS.topConceptOf, scheme))
    else:
        explicit_roots = set()
        explicit_roots.update(o for _, o in graph.subject_objects(SKOS.hasTopConcept))
        explicit_roots.update(s for s, _ in graph.subject_objects(SKOS.topConceptOf))

    return {concept for concept in explicit_roots if isinstance(concept, URIRef) and concept in concepts}


def hierarchy_roots(
    graph: Graph, concepts: set[URIRef], children: dict[URIRef, set[URIRef]], scheme: URIRef | None
) -> set[URIRef]:
    parented = {child for descendants in children.values() for child in descendants}
    explicit_roots = top_concepts(graph, concepts, scheme) - parented

    if explicit_roots:
        return explicit_roots

    roots = concepts - parented
    if roots:
        return roots

    return concepts


def label_for(graph: Graph, concept: URIRef, preferred_lang: str, show_iri: bool) -> str:
    labels = list(graph.objects(concept, SKOS.prefLabel))

    for label in labels:
        if getattr(label, "language", None) == preferred_lang:
            text = str(label)
            break
    else:
        for label in labels:
            if getattr(label, "language", None) is None:
                text = str(label)
                break
        else:
            text = str(labels[0]) if labels else graph.namespace_manager.normalizeUri(concept)

    if show_iri:
        return f"{text} <{concept}>"

    return text


def sort_concepts(graph: Graph, concepts: Iterable[URIRef], preferred_lang: str) -> list[URIRef]:
    return sorted(concepts, key=lambda concept: label_for(graph, concept, preferred_lang, False).lower())


def print_concept(
    graph: Graph,
    concept: URIRef,
    children: dict[URIRef, set[URIRef]],
    preferred_lang: str,
    show_iri: bool,
    depth: int = 0,
    path: tuple[URIRef, ...] = (),
) -> None:
    cycle = concept in path
    suffix = " [cycle]" if cycle else ""
    print(f"{INDENT * depth}- {label_for(graph, concept, preferred_lang, show_iri)}{suffix}")

    if cycle:
        return

    for child in sort_concepts(graph, children.get(concept, set()), preferred_lang):
        print_concept(graph, child, children, preferred_lang, show_iri, depth + 1, (*path, concept))


def print_hierarchy(graph: Graph, scheme: URIRef | None, relation: str, preferred_lang: str, show_iri: bool) -> None:
    concepts = concepts_for_scheme(graph, scheme)
    children = build_children(graph, concepts, relation)
    roots = hierarchy_roots(graph, concepts, children, scheme)

    print("Concept Hierarchy")
    if scheme is not None:
        print(f"Scheme: {scheme}")
    print()

    for root in sort_concepts(graph, roots, preferred_lang):
        print_concept(graph, root, children, preferred_lang, show_iri)


def main() -> None:
    args = parse_args()
    source = str(Path(args.vocabulary)) if Path(args.vocabulary).exists() else args.vocabulary
    scheme = URIRef(args.scheme) if args.scheme else None

    graph = load_graph(source, args.rdf_format)
    print_hierarchy(graph, scheme, args.relation, args.lang, args.show_iri)


if __name__ == "__main__":
    main()
