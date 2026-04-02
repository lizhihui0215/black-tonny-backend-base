from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read_doc(name: str) -> str:
    return (REPO_ROOT / "docs" / name).read_text(encoding="utf-8")


def test_capture_to_sales_orders_path_doc_keeps_first_path_noop_non_ready_and_failure_truth() -> None:
    text = read_doc("capture-to-sales-orders-path.md")

    assert "A minimal first `capture -> transform -> serving` path is now implemented" in text
    assert "- `capture_db`" in text
    assert "- `serving_db`" in text
    assert "`analysis_batches` remains outside the current admitted-input and readiness minimums." in text
    assert "- `status = \"noop\"`" in text
    assert "- `reason = \"missing_admitted_input\"`" in text
    assert "- `status = \"non_ready\"`" in text
    assert "- `reason = \"not_ready\"`" in text
    assert "- writes the current first-slice `sales_orders` projection rows on the serving database" in text
    assert "- writes `captured -> transformed` on the capture batch through the narrow lifecycle helper" in text
    assert "- no linked `analysis_batches` row is readable" in text
    assert "- the downstream `sales_orders` contract apply raises an exception" in text
    assert (
        "the current path rolls back the current serving-side transaction before it writes "
        "`captured -> failed` on the capture side"
        in text
    )
    assert (
        "- roll back serving-side partial writes before marking the batch as `failed` when the downstream contract "
        "apply fails mid-call"
        in text
    )


def test_capture_serving_boundary_and_sales_orders_contract_point_to_first_path() -> None:
    capture_serving_text = read_doc("capture-serving-boundary.md")
    sales_contract_text = read_doc("sales-orders-projection-contract.md")

    assert "For the current first minimal `capture -> transform -> serving` path" in capture_serving_text
    assert (
        "a minimal first `capture -> transform -> serving` path now exists in repo code for the `sales_orders` slice"
        in capture_serving_text
    )
    assert (
        "the current first `sales_orders` path may read capture and write serving through repo-internal services only"
        in capture_serving_text
    )
    assert "For the current first minimal end-to-end path that now invokes this contract" in sales_contract_text
    assert (
        "The current first capture-to-serving path now calls this contract through a separate narrower path service."
        in sales_contract_text
    )
