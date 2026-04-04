from dataclasses import dataclass
from typing import Final, Literal

_SLICE_NAME: Final[Literal["orders_first_adjacent_contract_implementation_preflight"]] = (
    "orders_first_adjacent_contract_implementation_preflight"
)
_CONTRACT_PREP_ANCHOR_NAME: Final[Literal["orders_first_adjacent_contract_prep_anchor"]] = (
    "orders_first_adjacent_contract_prep_anchor"
)
_SOURCE_ENDPOINT: Final[Literal["/erp/orders"]] = "/erp/orders"
_LANDED_ORDERS_CONTRACT: Final[Literal["sales_orders"]] = "sales_orders"
_TARGET_CANDIDATE_NAME: Final[str] = "sales_order_items-adjacent target candidate"
_SERVICE_ANCHOR_PATH: Final[str] = "src/app/services/orders_first_adjacent_contract_implementation_preflight.py"
_ALLOWED_FORMAL_DOC_PATHS: Final[tuple[str, str, str]] = (
    "docs/orders-first-adjacent-contract-questions.md",
    "docs/orders-first-adjacent-contract-baseline.md",
    "docs/orders-first-adjacent-scoped-contract-statement.md",
)
_COMPARISON_ANCHOR_PATHS: Final[tuple[str, str, str]] = (
    "src/app/models/sales_order_item.py",
    "src/app/schemas/sales.py",
    "src/app/crud/crud_sales_order_items.py",
)
_BLOCKERS: Final[tuple[str, ...]] = (
    "target_candidate_not_confirmed",
    "carrier_truth_not_formalized",
    "relation_truth_not_formalized",
    "detail_clue_truth_not_formalized",
    "identity_truth_not_formalized",
    "overwrite_upsert_truth_not_formalized",
    "path_and_behavior_truth_not_formalized",
)
_FORBIDDEN_TRUTHS: Final[tuple[str, ...]] = (
    "confirmed_first_adjacent_target_truth",
    "adjacent_identity_truth",
    "adjacent_non_identity_field_truth",
    "adjacent_overwrite_upsert_truth",
    "adjacent_write_helper_truth",
    "adjacent_path_helper_truth",
    "adjacent_runtime_binding_truth",
    "adjacent_migration_requirement_truth",
)


@dataclass(frozen=True, slots=True)
class OrdersFirstAdjacentContractPrepAnchor:
    anchor_name: Literal["orders_first_adjacent_contract_prep_anchor"]
    source_endpoint: str
    service_anchor_path: str
    allowed_formal_doc_paths: tuple[str, str, str]
    allowed_comparison_anchor_paths: tuple[str, str, str]
    current_landed_orders_contract: str
    target_candidate_name: str
    target_candidate_status: Literal["candidate_only"]
    allows_contract_writes: bool
    allows_migration_changes: bool
    allows_runtime_binding: bool
    blockers: tuple[str, ...]
    forbidden_truths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OrdersFirstAdjacentContractImplementationPreflight:
    slice_name: Literal["orders_first_adjacent_contract_implementation_preflight"]
    source_endpoint: str
    current_landed_orders_contract: str
    target_candidate_name: str
    service_anchor_path: str
    comparison_anchor_paths: tuple[str, str, str]
    allows_contract_writes: bool
    allows_migration_changes: bool
    allows_runtime_binding: bool
    blockers: tuple[str, ...]
    contract_prep_anchor: OrdersFirstAdjacentContractPrepAnchor


_CONTRACT_PREP_ANCHOR = OrdersFirstAdjacentContractPrepAnchor(
    anchor_name=_CONTRACT_PREP_ANCHOR_NAME,
    source_endpoint=_SOURCE_ENDPOINT,
    service_anchor_path=_SERVICE_ANCHOR_PATH,
    allowed_formal_doc_paths=_ALLOWED_FORMAL_DOC_PATHS,
    allowed_comparison_anchor_paths=_COMPARISON_ANCHOR_PATHS,
    current_landed_orders_contract=_LANDED_ORDERS_CONTRACT,
    target_candidate_name=_TARGET_CANDIDATE_NAME,
    target_candidate_status="candidate_only",
    allows_contract_writes=False,
    allows_migration_changes=False,
    allows_runtime_binding=False,
    blockers=_BLOCKERS,
    forbidden_truths=_FORBIDDEN_TRUTHS,
)


_PREFLIGHT_SUMMARY = OrdersFirstAdjacentContractImplementationPreflight(
    slice_name=_SLICE_NAME,
    source_endpoint=_SOURCE_ENDPOINT,
    current_landed_orders_contract=_LANDED_ORDERS_CONTRACT,
    target_candidate_name=_TARGET_CANDIDATE_NAME,
    service_anchor_path=_SERVICE_ANCHOR_PATH,
    comparison_anchor_paths=_COMPARISON_ANCHOR_PATHS,
    allows_contract_writes=False,
    allows_migration_changes=False,
    allows_runtime_binding=False,
    blockers=_BLOCKERS,
    contract_prep_anchor=_CONTRACT_PREP_ANCHOR,
)


def get_orders_first_adjacent_contract_implementation_preflight(
) -> OrdersFirstAdjacentContractImplementationPreflight:
    return _PREFLIGHT_SUMMARY


def get_orders_first_adjacent_contract_prep_anchor() -> OrdersFirstAdjacentContractPrepAnchor:
    return _CONTRACT_PREP_ANCHOR
