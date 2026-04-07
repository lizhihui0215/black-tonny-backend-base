from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTELLIGENCE_ROOT = REPO_ROOT / "docs" / "source-intelligence"


def assert_relative_link_exists(doc_path: Path, relative_link: str) -> None:
    target = (doc_path.parent / relative_link).resolve()
    assert target.exists(), f"{doc_path} points to missing target: {relative_link}"


def test_source_intelligence_spine_files_exist() -> None:
    assert (SOURCE_INTELLIGENCE_ROOT / "README.md").exists()
    assert (SOURCE_INTELLIGENCE_ROOT / "AGENTS.md").exists()
    assert (SOURCE_INTELLIGENCE_ROOT / "ops" / "README.md").exists()
    assert (SOURCE_INTELLIGENCE_ROOT / "ops" / "current-main-state.md").exists()
    assert (SOURCE_INTELLIGENCE_ROOT / "ops" / "review-gain-ledger.md").exists()
    assert (REPO_ROOT / "docs" / "reference" / "legacy-backend" / "extracts" / "README.md").exists()


def test_source_intelligence_readme_keeps_core_spine_links_and_drops_known_missing_doc() -> None:
    readme_path = SOURCE_INTELLIGENCE_ROOT / "README.md"
    text = readme_path.read_text(encoding="utf-8")

    assert "[AGENTS.md](./AGENTS.md)" in text
    assert "[ops/README.md](./ops/README.md)" in text
    assert "[../reference/legacy-backend/extracts/README.md](../reference/legacy-backend/extracts/README.md)" in text
    assert "[sales-order-items-projection-contract.md](" not in text

    assert_relative_link_exists(readme_path, "./AGENTS.md")
    assert_relative_link_exists(readme_path, "./ops/README.md")
    assert_relative_link_exists(readme_path, "../reference/legacy-backend/extracts/README.md")


def test_source_intelligence_readme_discovers_ops_as_control_plane_not_output_slot() -> None:
    readme_path = SOURCE_INTELLIGENCE_ROOT / "README.md"
    text = readme_path.read_text(encoding="utf-8")

    for fragment in (
        "current main state",
        "review gain ledger",
        "milestone tracking",
        "handoff",
        "quality gates",
    ):
        assert fragment in text

    assert "不是新的" in text
    for fragment in ("dossier", "field dictionary", "relation", "serving-readiness", "正文输出位"):
        assert fragment in text


def test_ops_readme_keeps_boundary_links_and_merge_update_rule() -> None:
    readme_path = SOURCE_INTELLIGENCE_ROOT / "ops" / "README.md"
    text = readme_path.read_text(encoding="utf-8")

    for relative_link in (
        "../apis/README.md",
        "../fields/README.md",
        "../relations/README.md",
        "../serving-readiness/README.md",
        "./current-main-state.md",
        "./review-gain-ledger.md",
    ):
        assert_relative_link_exists(readme_path, relative_link)

    assert "[../apis/README.md](../apis/README.md)" in text
    assert "[../fields/README.md](../fields/README.md)" in text
    assert "[../relations/README.md](../relations/README.md)" in text
    assert "[../serving-readiness/README.md](../serving-readiness/README.md)" in text
    assert "[current-main-state.md](./current-main-state.md)" in text
    assert "[review-gain-ledger.md](./review-gain-ledger.md)" in text
    assert "merge 后" in text
    assert "current main state" in text
    assert "review gain ledger" in text
    for fragment in ("新的正文输出位", "field dictionary", "relation doc", "serving-readiness doc"):
        assert fragment in text
