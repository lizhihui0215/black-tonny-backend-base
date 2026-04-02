from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read_doc(name: str) -> str:
    return (REPO_ROOT / "docs" / name).read_text(encoding="utf-8")


def test_sales_orders_projection_contract_doc_keeps_first_slice_identity_and_overwrite_truth() -> None:
    text = read_doc("sales-orders-projection-contract.md")

    assert "A minimal first-slice `sales_orders` serving projection contract is now implemented" in text
    assert "- one `sales_orders` projection row per `analysis_batch_id + order_id`" in text
    assert "- `sales_orders` now keeps a unique constraint on `analysis_batch_id + order_id`" in text
    assert (
        "the current serving migration assumes the existing `sales_orders` table does not already contain duplicate "
        "`analysis_batch_id + order_id` pairs"
        in text
    )
    assert "a dedicated dedupe migration must run before the current unique constraint can be applied safely" in text
    assert "the last fact in input order wins" in text
    assert "- one current contract apply call runs inside one serving-side transaction" in text
    assert (
        "the helper rolls back the current serving-side writes from that apply call before it re-raises the failure"
        in text
    )
    assert "- the current contract requires callers to provide `payment_status` explicitly" in text
    assert "- overwrite `capture_batch_id`" in text
    assert "- overwrite `paid_amount`" in text
    assert "They are not the current first-slice contract helper" in text
    assert "It does not define:" in text
    assert "- a full transform executor" in text
    assert "- roll back serving-side writes from one apply call when a later write in the same call fails" in text


def test_serving_projection_minimal_boundary_points_to_first_sales_orders_contract() -> None:
    text = read_doc("serving-projection-minimal-boundary.md")

    assert (
        "For the current first `sales_orders` serving projection contract layered on top of this persistence surface"
        in text
    )
    assert "- the first `sales_orders` serving projection contract helper and its persistence constraint" in text
    assert "no upsert helpers beyond the current first `sales_orders` contract helper" in text
    assert (
        "any projection identity or upsert contract beyond the current first `sales_orders` slice is finalized"
        in text
    )
    assert (
        "the current first-slice identity migration assumes the existing `sales_orders` table does not already "
        "contain duplicate `analysis_batch_id + order_id` pairs"
        in text
    )
