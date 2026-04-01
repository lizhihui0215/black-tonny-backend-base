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


def test_transform_state_transition_boundary_keeps_future_constraints_without_transition_proof_claims() -> None:
    text = read_doc("transform-state-transition-boundary.md")

    assert "these lifecycle-transition minimums are future formal constraints only." in text
    assert (
        "They do not mean that any lifecycle transition has already been proven, executed, scheduled, reserved, or "
        "coordinated."
        in text
    )
    assert (
        "`analysis_batches` is not a current minimum prerequisite or proof source for transform lifecycle transitions."
        in text
    )
    assert "`capture_batches.batch_status` does not prove that a formal lifecycle transition has occurred" in text
    assert "`capture_batches.transformed_at` does not prove that a formal completion transition has occurred" in text
    assert (
        "`capture_batches.error_message` does not prove that a formal failed or terminal transition has been declared"
        in text
    )
    assert (
        "`capture_batches.updated_at` does not prove transition progress, transition ordering, reservation, or "
        "execution"
        in text
    )


def test_capture_batch_field_semantics_keep_lifecycle_transition_non_proof_boundary() -> None:
    text = read_doc("capture-batch-field-semantics.md")

    assert "No selector, lifecycle helper, transition executor, or scheduler currently owns them either." in text
    assert "- not proof that a formal lifecycle transition has occurred" in text
    assert "- not proof of a formal lifecycle transition completion" in text
    assert "- not proof that a failed or terminal lifecycle transition has been formally declared" in text
    assert "- not proof that a lifecycle transition was executed, scheduled, or reserved" in text
