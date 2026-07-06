"""Build knowledge graph nodes and edges from AtlasX outputs."""

from __future__ import annotations

from atlasx.models.evidence import EvidenceAppraisal
from atlasx.models.graph import GraphEdge, GraphNode
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.models.paper import PaperDocument
from atlasx.utils.hashing import stable_id


def build_graph(
    *,
    documents: list[PaperDocument],
    atoms_by_paper: dict[str, list[KnowledgeAtom]],
    concepts: list[dict[str, object]],
    evidence_appraisals: list[EvidenceAppraisal],
    connections: list[dict[str, object]],
    gaps: list[dict[str, object]],
    directions: list[dict[str, object]],
) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Create graph rows for CSV export."""

    nodes: dict[str, GraphNode] = {}
    edges: dict[str, GraphEdge] = {}

    def add_node(node: GraphNode) -> str:
        nodes.setdefault(node.node_id, node)
        return node.node_id

    def add_edge(edge: GraphEdge) -> None:
        edges.setdefault(edge.edge_id, edge)

    for document in documents:
        metadata = document.metadata
        paper_node = add_node(
            GraphNode(
                node_id=f"paper_{metadata.paper_id}",
                node_type="Paper",
                label=metadata.title,
                paper_id=metadata.paper_id,
                source_trace=metadata.file,
                confidence=0.9,
                properties={
                    "doi": metadata.doi or "not reported",
                    "year": str(metadata.year or "not reported"),
                    "source_type": metadata.source_type,
                },
            )
        )
        if metadata.journal != "unknown":
            journal_node = add_node(
                GraphNode(
                    node_id=stable_id("journal", metadata.journal),
                    node_type="Journal",
                    label=metadata.journal,
                    paper_id=metadata.paper_id,
                    source_trace=metadata.file,
                    confidence=0.8,
                )
            )
            add_edge(_edge(paper_node, journal_node, "PAPER_PUBLISHED_IN", metadata.paper_id, metadata.file))
        for author in metadata.authors:
            author_node = add_node(
                GraphNode(
                    node_id=stable_id("author", author),
                    node_type="Author",
                    label=author,
                    paper_id=metadata.paper_id,
                    source_trace=metadata.file,
                    confidence=0.8,
                )
            )
            add_edge(_edge(author_node, paper_node, "AUTHOR_OF_PAPER", metadata.paper_id, metadata.file))

    evidence_by_atom = {item.atom_id: item for item in evidence_appraisals}
    gap_by_atom = {str(item["atom_id"]): item for item in gaps}
    direction_by_atom = {str(item["atom_id"]): item for item in directions}

    for paper_id, atoms in atoms_by_paper.items():
        paper_node = f"paper_{paper_id}"
        for atom in atoms:
            question_node = add_node(
                GraphNode(
                    node_id=stable_id("question", atom.paper_question),
                    node_type="ResearchQuestion",
                    label=atom.paper_question,
                    paper_id=paper_id,
                    source_trace=atom.source_trace,
                    confidence=atom.confidence,
                )
            )
            entity_node = add_node(_atom_node("Entity", atom.entity, paper_id, atom))
            input_node = add_node(_atom_node("Input", atom.input_signal_or_intervention, paper_id, atom))
            condition_node = add_node(_atom_node("Condition", atom.condition, paper_id, atom))
            mechanism_node = add_node(_atom_node("Mechanism", atom.mechanism, paper_id, atom))
            outcome_node = add_node(_atom_node("Outcome", atom.outcome, paper_id, atom))
            evidence_node = add_node(
                GraphNode(
                    node_id=stable_id("evidence", atom.atom_id, atom.evidence_statement),
                    node_type="EvidenceUnit",
                    label=atom.evidence_statement,
                    paper_id=paper_id,
                    source_trace=atom.source_trace,
                    confidence=atom.confidence,
                    properties={"evidence_type": atom.evidence_type},
                )
            )
            gap_record = gap_by_atom.get(atom.atom_id)
            gap_label = str(gap_record["gap"]) if gap_record else atom.gap
            gap_node = add_node(_simple_node("Gap", gap_label, paper_id, atom.source_trace, atom.confidence))
            direction_record = direction_by_atom.get(atom.atom_id)
            direction_label = (
                str(direction_record["candidate_review_topic"])
                if direction_record
                else atom.next_step
            )
            direction_node = add_node(
                _simple_node(
                    "DiscoveryDirection",
                    direction_label,
                    paper_id,
                    atom.source_trace,
                    min(atom.confidence, 0.55),
                )
            )
            claim_node = add_node(
                GraphNode(
                    node_id=atom.atom_id,
                    node_type="Claim",
                    label=atom.evidence_statement,
                    paper_id=paper_id,
                    source_trace=atom.source_trace,
                    confidence=atom.confidence,
                )
            )

            add_edge(_edge(paper_node, question_node, "PAPER_ASKS_QUESTION", paper_id, atom.source_trace))
            add_edge(_edge(paper_node, entity_node, "PAPER_TESTS_ENTITY", paper_id, atom.source_trace))
            add_edge(_edge(paper_node, input_node, "PAPER_APPLIES_INPUT", paper_id, atom.source_trace))
            add_edge(_edge(input_node, condition_node, "INPUT_UNDER_CONDITION", paper_id, atom.source_trace))
            add_edge(_edge(claim_node, mechanism_node, "CLAIM_SUPPORTS_MECHANISM", paper_id, atom.source_trace))
            add_edge(_edge(mechanism_node, outcome_node, "MECHANISM_ASSOCIATED_WITH_OUTCOME", paper_id, atom.source_trace))
            add_edge(_edge(evidence_node, claim_node, "EVIDENCE_SUPPORTS_CLAIM", paper_id, atom.source_trace))
            add_edge(_edge(paper_node, gap_node, "PAPER_HAS_GAP", paper_id, atom.source_trace))
            add_edge(
                _edge(
                    gap_node,
                    direction_node,
                    "GAP_POINTS_TO_DISCOVERY_DIRECTION",
                    paper_id,
                    atom.source_trace,
                )
            )
            appraisal = evidence_by_atom.get(atom.atom_id)
            if appraisal:
                nodes[evidence_node].properties["limitations"] = "; ".join(appraisal.limitations)

    concept_nodes: list[str] = []
    for concept in concepts:
        label = str(concept["canonical_concept"])
        concept_node = add_node(
            GraphNode(
                node_id=str(concept["concept_id"]),
                node_type="Concept",
                label=label,
                source_trace=str(concept.get("source_trace", "derived from atoms")),
                confidence=float(concept.get("confidence", 0.5)),
                properties={
                    "uncertainty": str(concept.get("uncertainty", "requires review")),
                    "broader": str(concept.get("broader", "unknown")),
                    "narrower": str(concept.get("narrower", "unknown")),
                },
            )
        )
        concept_nodes.append(concept_node)

    for left, right in zip(concept_nodes, concept_nodes[1:]):
        add_edge(_edge(left, right, "CONCEPT_RELATED_TO", None, "derived ontology mapping"))

    for connection in connections:
        left = f"paper_{connection['source_paper_id']}"
        right = f"paper_{connection['target_paper_id']}"
        edge_type = (
            "PAPER_CONTRADICTS_PAPER"
            if "contradict" in str(connection["connection_type"]).lower()
            else "PAPER_CONNECTS_TO_PAPER"
        )
        add_edge(
            GraphEdge(
                edge_id=str(connection["connection_id"]),
                source_id=left,
                target_id=right,
                edge_type=edge_type,
                label=str(connection["connection_type"]),
                source_trace=str(connection["source_trace"]),
                confidence=float(connection["confidence"]),
                evidence=", ".join(str(term) for term in connection["shared_terms"]),
            )
        )

    return list(nodes.values()), list(edges.values())


def _atom_node(node_type: str, label: str, paper_id: str, atom: KnowledgeAtom) -> GraphNode:
    return _simple_node(node_type, label, paper_id, atom.source_trace, atom.confidence)


def _simple_node(
    node_type: str,
    label: str,
    paper_id: str | None,
    source_trace: str,
    confidence: float,
) -> GraphNode:
    return GraphNode(
        node_id=stable_id(node_type.lower(), label, paper_id or ""),
        node_type=node_type,
        label=label,
        paper_id=paper_id,
        source_trace=source_trace,
        confidence=confidence,
    )


def _edge(
    source_id: str,
    target_id: str,
    edge_type: str,
    paper_id: str | None,
    source_trace: str,
) -> GraphEdge:
    return GraphEdge(
        edge_id=stable_id("edge", source_id, target_id, edge_type, paper_id or ""),
        source_id=source_id,
        target_id=target_id,
        edge_type=edge_type,
        label=edge_type.replace("_", " ").title(),
        paper_id=paper_id,
        source_trace=source_trace,
        confidence=0.6,
    )

