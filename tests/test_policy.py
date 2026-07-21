from pathlib import Path

import pytest

from harnessie_engine_wrappers.policy import UnsafePolicy, load_policy_file, normalize_paths


def test_normalize_rejects_root_and_home():
    with pytest.raises(UnsafePolicy):
        normalize_paths([str(Path("/"))])
    with pytest.raises(UnsafePolicy):
        normalize_paths([str(Path.home())])


def test_normalize_rejects_multiline_and_empty():
    with pytest.raises(UnsafePolicy):
        normalize_paths(["x\ny"])
    with pytest.raises(UnsafePolicy):
        normalize_paths([])


def test_policy_file_ignores_comments_and_blanks(tmp_path):
    policy = tmp_path / "policy.txt"
    policy.write_text("# comment\n\n~/.ssh\n", encoding="utf-8")
    assert load_policy_file(policy) == ("~/.ssh",)
