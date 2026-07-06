from atlasx.graph.builder import build_graph
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.models.paper import PaperDocument, PaperMetadata


def test_graph_builder_creates_nodes_and_edges() -> None:
    document = PaperDocument(
        metadata=PaperMetadata(
            paper_id="paper_1",
            title="Toy Paper",
            authors=["A. Author"],
            journal="Toy Journal",
            file="toy.txt",
        ),
        text="Toy text",
        chunks=[],
    )
    atom = KnowledgeAtom(
        atom_id="atom_1",
        paper_id="paper_1",
        source_trace="toy.txt; chunk 1",
        paper_question="What changes?",
        entity="toy cells",
        input_signal_or_intervention="field exposure",
        condition="not reported",
        mechanism="membrane voltage",
        outcome="cell proliferation",
        evidence_statement="Toy evidence.",
        evidence_type="in vitro",
        gap="replication not reported",
        connection_candidates=["membrane voltage"],
    )

    nodes, edges = build_graph(
        documents=[document],
        atoms_by_paper={"paper_1": [atom]},
        concepts=[],
        evidence_appraisals=[],
        connections=[],
        gaps=[],
        directions=[],
    )

    assert any(node.node_type == "Paper" for node in nodes)
    assert any(node.node_type == "Mechanism" for node in nodes)
    assert any(edge.edge_type == "PAPER_ASKS_QUESTION" for edge in edges)
    assert any(edge.edge_type == "EVIDENCE_SUPPORTS_CLAIM" for edge in edges)

