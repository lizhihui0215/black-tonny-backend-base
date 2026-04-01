from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read_doc(name: str) -> str:
    return (REPO_ROOT / "docs" / name).read_text(encoding="utf-8")


def test_transform_input_boundary_keeps_capture_side_candidate_floor() -> None:
    text = read_doc("transform-input-boundary.md")

    assert "- one persisted `capture_batches` row" in text
    assert (
        "- one or more persisted `capture_endpoint_payloads` rows linked to that batch through `capture_batch_id`"
        in text
    )
    assert "`analysis_batches` is already a landed persisted context table" in text
    assert "it is not part of the current minimum transform input candidate boundary" in text


def test_admitted_transform_input_boundary_keeps_analysis_optional_and_status_non_admitting() -> None:
    text = read_doc("admitted-transform-input-boundary.md")

    assert "`analysis_batches` is not a current minimum prerequisite for admitted transform input." in text
    assert "No current `batch_status` value, including `captured`, is by itself a formal admission marker." in text
    assert "Current admitted-input minimums also do not reinterpret `transformed_at` as admission proof." in text


def test_transform_readiness_boundary_keeps_structural_floor_without_execution_claims() -> None:
    text = read_doc("transform-readiness-boundary.md")

    assert "`analysis_batches` is not a current minimum prerequisite for transform readiness." in text
    assert (
        "readiness only means that the admitted input set satisfies the minimum formal persisted-input conditions."
        in text
    )
    assert (
        "It does not mean that transform has run, been scheduled, been reserved, or will necessarily execute."
        in text
    )
    assert "No current `batch_status` value, including `captured`, is by itself a formal readiness marker." in text
    assert "Current readiness minimums also do not reinterpret `transformed_at` as readiness proof." in text
