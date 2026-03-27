#!/usr/bin/env python3
"""Thin shared helpers for repo-local collaboration scripts."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_CANDIDATES = ("origin/main", "main")


class GitCommandError(RuntimeError):
    """Raised when a git command fails."""


@dataclass(frozen=True)
class ComparisonSpec:
    base_ref: str
    merge_base: str
    mode: str


def build_common_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--base",
        help="Git base ref to compare against. Defaults to origin/main, then main.",
    )
    parser.add_argument(
        "--mode",
        choices=("head", "worktree"),
        default="head",
        help="Compare committed HEAD only, or include tracked worktree changes.",
    )
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Print output only and skip pbcopy even if it is available.",
    )
    return parser


def run_git(args: list[str], check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    if check and completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise GitCommandError(message)
    return completed.stdout


def ensure_git_repo() -> None:
    completed = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "not a git repository"
        raise GitCommandError(message)


def ref_exists(ref: str) -> bool:
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    return completed.returncode == 0


def resolve_base_ref(explicit_ref: str | None) -> str:
    ensure_git_repo()
    if explicit_ref:
        if ref_exists(explicit_ref):
            return explicit_ref
        raise GitCommandError(f"base ref not found: {explicit_ref}")

    for candidate in DEFAULT_BASE_CANDIDATES:
        if ref_exists(candidate):
            return candidate

    raise GitCommandError("could not resolve base ref; tried origin/main and main")


def resolve_comparison(base_ref: str | None, mode: str) -> ComparisonSpec:
    resolved_base = resolve_base_ref(base_ref)
    merge_base = run_git(["merge-base", resolved_base, "HEAD"]).strip()
    if not merge_base:
        raise GitCommandError(f"could not resolve merge-base for {resolved_base} and HEAD")
    return ComparisonSpec(base_ref=resolved_base, merge_base=merge_base, mode=mode)


def get_untracked_files() -> list[str]:
    return [line for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines() if line]


def get_changed_paths(spec: ComparisonSpec) -> list[str]:
    if spec.mode == "head":
        lines = run_git(["diff", "--name-only", f"{spec.merge_base}...HEAD"]).splitlines()
        return [line for line in lines if line]

    tracked = [line for line in run_git(["diff", "--name-only", spec.merge_base]).splitlines() if line]
    return dedupe_preserve_order(tracked + get_untracked_files())


def get_changed_status_lines(spec: ComparisonSpec) -> list[str]:
    if spec.mode == "head":
        lines = run_git(["diff", "--name-status", f"{spec.merge_base}...HEAD"]).splitlines()
        return [line for line in lines if line]

    tracked = [line for line in run_git(["diff", "--name-status", spec.merge_base]).splitlines() if line]
    untracked = [f"??\t{path}" for path in get_untracked_files()]
    return dedupe_preserve_order(tracked + untracked)


def get_diff_text(spec: ComparisonSpec) -> str:
    if spec.mode == "head":
        diff_text = run_git(["diff", "--no-ext-diff", "--binary", f"{spec.merge_base}...HEAD"])
        return diff_text

    tracked_diff = run_git(["diff", "--no-ext-diff", "--binary", spec.merge_base]).rstrip()
    untracked_diffs: list[str] = []
    for path in get_untracked_files():
        completed = subprocess.run(
            ["git", "diff", "--no-index", "--binary", "--", "/dev/null", path],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )
        if completed.returncode not in (0, 1):
            message = completed.stderr.strip() or completed.stdout.strip() or f"could not diff untracked file: {path}"
            raise GitCommandError(message)
        patch_text = completed.stdout.rstrip()
        if patch_text:
            untracked_diffs.append(patch_text)

    parts = [part for part in [tracked_diff, *untracked_diffs] if part]
    if not parts:
        return ""
    return "\n\n".join(parts) + "\n"


def copy_to_clipboard(text: str, enabled: bool) -> str:
    if not enabled:
        return "clipboard skipped (--no-clipboard)"

    pbcopy = shutil.which("pbcopy")
    if not pbcopy:
        return "clipboard skipped (pbcopy not available)"

    completed = subprocess.run([pbcopy], input=text, text=True, capture_output=True)
    if completed.returncode == 0:
        return "clipboard copied via pbcopy"

    message = completed.stderr.strip() or completed.stdout.strip() or "pbcopy failed"
    return f"clipboard copy failed ({message})"


def emit_output(text: str, spec: ComparisonSpec | None, clipboard_enabled: bool) -> int:
    status = copy_to_clipboard(text, enabled=clipboard_enabled)
    if spec is not None:
        print(
            f"[mode={spec.mode}] [base_ref={spec.base_ref}] [merge_base={spec.merge_base}]",
            file=sys.stderr,
        )
    print(f"[{status}]", file=sys.stderr)
    sys.stdout.write(text)
    if text and not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


def format_metadata_block(spec: ComparisonSpec, tool_name: str) -> str:
    return "\n".join(
        [
            f"# tool: {tool_name}",
            f"# mode: {spec.mode}",
            f"# base ref: {spec.base_ref}",
            f"# merge base: {spec.merge_base}",
        ]
    )


def dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def format_bullets(items: list[str]) -> str:
    if not items:
        return "- 待人工补充"
    return "\n".join(f"- {item}" for item in items)


def has_prefix(paths: list[str], prefixes: tuple[str, ...]) -> bool:
    return any(path.startswith(prefixes) for path in paths)


def boundary_flags(paths: list[str]) -> dict[str, bool]:
    return {
        "research": any("research" in path for path in paths) or has_prefix(paths, ("docs/erp/",)),
        "capture": any("capture" in path for path in paths)
        or has_prefix(paths, ("src/migrations/capture_versions/", "docs/capture")),
        "serving": any("serving" in path for path in paths),
        "runtime": has_prefix(paths, ("src/app/", "src/api/", "src/core/", "src/scripts/")),
        "api_behavior": has_prefix(paths, ("src/app/api/", "src/app/routes/", "src/api/")),
    }


def default_old_repo() -> Path | None:
    candidate = REPO_ROOT.parent / "black-tonny-backend"
    if candidate.exists():
        return candidate
    return None


def run_cli(entrypoint: Callable[[], int]) -> int:
    try:
        return entrypoint()
    except GitCommandError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
