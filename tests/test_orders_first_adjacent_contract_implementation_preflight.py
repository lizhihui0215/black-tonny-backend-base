from pathlib import Path

from src.app.services.orders_first_adjacent_contract_implementation_preflight import (
    get_orders_first_adjacent_contract_implementation_preflight,
    get_orders_first_adjacent_contract_prep_anchor,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_orders_first_adjacent_contract_implementation_preflight_stays_narrow() -> None:
    docs_index_text = read_text("docs/README.md")
    doc_text = read_text("docs/orders-first-adjacent-contract-implementation-preflight.md")
    preflight = get_orders_first_adjacent_contract_implementation_preflight()
    contract_prep_anchor = get_orders_first_adjacent_contract_prep_anchor()

    assert "orders-first-adjacent-contract-implementation-preflight.md" in docs_index_text
    assert "No adjacent `/erp/orders` contract is currently implemented or finalized" in doc_text
    assert "One minimal, reversible implementation-preflight slice now exists." in doc_text
    assert "The current preflight-only service anchor may narrow one step further into one contract-prep anchor." in doc_text
    assert "- it is non-writing" in doc_text
    assert "- it is non-migrating" in doc_text
    assert "- it is non-runtime-binding" in doc_text
    assert "This is the narrowest anchor surface currently admitted by formal truth." in doc_text
    assert "src/app/services/orders_first_adjacent_contract_implementation_preflight.py" in doc_text
    assert "docs/orders-first-adjacent-contract-questions.md" in doc_text
    assert "docs/orders-first-adjacent-contract-baseline.md" in doc_text
    assert "docs/orders-first-adjacent-scoped-contract-statement.md" in doc_text
    assert "src/app/models/sales_order_item.py" in doc_text
    assert "src/app/schemas/sales.py" in doc_text
    assert "src/app/crud/crud_sales_order_items.py" in doc_text
    assert "No broader comparison-anchor set is admitted by this slice." in doc_text
    assert "Migrations stay unchanged by default for this contract-prep anchor slice." in doc_text
    assert "`sales_order_items-adjacent target candidate` still remains candidate-only" in doc_text
    assert "- source-side carrier truth is not yet formalized for the adjacent lane" in doc_text
    assert "- adjacent overwrite and upsert rules are not yet formalized" in doc_text
    assert "- adjacent runtime-binding truth" in doc_text
    assert "- a migration is already required for the current contract-prep anchor slice" in doc_text

    assert preflight.slice_name == "orders_first_adjacent_contract_implementation_preflight"
    assert preflight.source_endpoint == "/erp/orders"
    assert preflight.current_landed_orders_contract == "sales_orders"
    assert preflight.target_candidate_name == "sales_order_items-adjacent target candidate"
    assert (
        preflight.service_anchor_path
        == "src/app/services/orders_first_adjacent_contract_implementation_preflight.py"
    )
    assert preflight.comparison_anchor_paths == (
        "src/app/models/sales_order_item.py",
        "src/app/schemas/sales.py",
        "src/app/crud/crud_sales_order_items.py",
    )
    assert preflight.allows_contract_writes is False
    assert preflight.allows_migration_changes is False
    assert preflight.allows_runtime_binding is False
    assert "identity_truth_not_formalized" in preflight.blockers
    assert "overwrite_upsert_truth_not_formalized" in preflight.blockers
    assert contract_prep_anchor.anchor_name == "orders_first_adjacent_contract_prep_anchor"
    assert contract_prep_anchor.source_endpoint == "/erp/orders"
    assert (
        contract_prep_anchor.service_anchor_path
        == "src/app/services/orders_first_adjacent_contract_implementation_preflight.py"
    )
    assert contract_prep_anchor.allowed_formal_doc_paths == (
        "docs/orders-first-adjacent-contract-questions.md",
        "docs/orders-first-adjacent-contract-baseline.md",
        "docs/orders-first-adjacent-scoped-contract-statement.md",
    )
    assert contract_prep_anchor.allowed_comparison_anchor_paths == (
        "src/app/models/sales_order_item.py",
        "src/app/schemas/sales.py",
        "src/app/crud/crud_sales_order_items.py",
    )
    assert contract_prep_anchor.current_landed_orders_contract == "sales_orders"
    assert contract_prep_anchor.target_candidate_name == "sales_order_items-adjacent target candidate"
    assert contract_prep_anchor.target_candidate_status == "candidate_only"
    assert contract_prep_anchor.allows_contract_writes is False
    assert contract_prep_anchor.allows_migration_changes is False
    assert contract_prep_anchor.allows_runtime_binding is False
    assert "path_and_behavior_truth_not_formalized" in contract_prep_anchor.blockers
    assert "confirmed_first_adjacent_target_truth" in contract_prep_anchor.forbidden_truths
    assert "adjacent_write_helper_truth" in contract_prep_anchor.forbidden_truths
    assert "adjacent_runtime_binding_truth" in contract_prep_anchor.forbidden_truths
