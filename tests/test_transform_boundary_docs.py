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

    assert "A minimal admitted transform input selector is now implemented in `black-tonny-backend-base`." in text
    assert "`analysis_batches` is not a current minimum prerequisite for admitted transform input." in text
    assert "No current `batch_status` value, including `captured`, is by itself a formal admission marker." in text
    assert "Current admitted-input minimums also do not reinterpret `transformed_at` as admission proof." in text
    assert "- does not gate on `batch_status`" in text
    assert "- does not gate on `transformed_at`" in text


def test_transform_readiness_boundary_keeps_structural_floor_without_execution_claims() -> None:
    text = read_doc("transform-readiness-boundary.md")

    assert "A minimal transform readiness evaluator is now implemented in `black-tonny-backend-base`." in text
    assert "`analysis_batches` is not a current minimum prerequisite for transform readiness." in text
    assert (
        "readiness only means that the admitted input set satisfies the current minimum formal persisted-input "
        "conditions for the current first slice."
        in text
    )
    assert "- the narrow `sales_orders` source slice" in text
    assert "- requires the admitted batch snapshot to keep `batch_status == \"captured\"`" in text
    assert "- requires the admitted batch snapshot to keep `transformed_at is None`" in text
    assert "- does not gate on `error_message`" in text
    assert (
        "It does not mean that transform has run, been scheduled, been reserved, or will necessarily execute."
        in text
    )
    assert (
        "No current field, including `batch_status` and `transformed_at`, is by itself a formal readiness proof."
        in text
    )


def test_transform_state_transition_boundary_keeps_future_constraints_without_transition_proof_claims() -> None:
    text = read_doc("transform-state-transition-boundary.md")

    assert "A minimal capture-batch lifecycle helper is now implemented in `black-tonny-backend-base`." in text
    assert (
        "broader lifecycle-transition minimums remain future formal constraints beyond the current first helper."
        in text
    )
    assert (
        "They do not mean that any broader lifecycle transition graph has already been proven, executed, scheduled, "
        "reserved, or coordinated."
        in text
    )
    assert (
        "`analysis_batches` is not a current minimum prerequisite or proof source for transform lifecycle transitions."
        in text
    )
    assert "`mark_capture_batch_transformed` writes only:" in text
    assert "`mark_capture_batch_failed` writes only:" in text
    assert (
        "both helper functions raise `ValueError` when the current batch row is not in the `captured` source state"
        in text
    )
    assert (
        "`capture_batches.batch_status` does not by itself prove that a formal lifecycle transition has occurred"
        in text
    )
    assert (
        "`capture_batches.transformed_at` does not by itself prove that a formal completion transition has occurred"
        in text
    )
    assert (
        "`capture_batches.error_message` does not by itself prove that a formal failed or terminal transition has "
        "been declared"
        in text
    )
    assert (
        "`capture_batches.updated_at` does not prove transition progress, transition ordering, reservation, or "
        "execution"
        in text
    )


def test_capture_batch_field_semantics_keep_lifecycle_transition_non_proof_boundary() -> None:
    text = read_doc("capture-batch-field-semantics.md")

    assert (
        "A minimal transform readiness evaluator and a minimal capture-batch lifecycle helper now read or write a "
        "narrow subset of these fields for the current first transform slice."
        in text
    )
    assert "- used by the current first-slice readiness evaluator as a required `captured` source-state gate" in text
    assert "- writable by the current lifecycle helper when one `captured` batch is marked `transformed`" in text
    assert "- overwritable by the current lifecycle helper when one `captured` batch is marked `failed`" in text
    assert "- not by itself proof that a formal lifecycle transition has occurred" in text
    assert "- not by itself proof of a formal lifecycle transition completion" in text
    assert "- not by itself proof that a failed or terminal lifecycle transition has been formally declared" in text
    assert "- not proof that a lifecycle transition was executed, scheduled, or reserved" in text
