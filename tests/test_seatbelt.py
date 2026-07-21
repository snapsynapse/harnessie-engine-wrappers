from pathlib import Path

from harnessie_engine_wrappers import seatbelt
from harnessie_engine_wrappers.seatbelt import profile_for


def test_profile_is_narrow_and_escapes_paths():
    profile = profile_for([Path('/tmp/credential "store"')])
    assert "(allow default)" in profile
    assert "deny file-read*" in profile
    assert '\\"store\\"' in profile
    assert "deny network" not in profile


def test_profile_has_one_rule_per_deny_path():
    profile = profile_for([Path("/tmp/a"), Path("/tmp/b")])
    assert profile.count("deny file-read*") == 2


def test_admission_failure_is_not_mistaken_for_containment(monkeypatch):
    class Result:
        returncode = 71
        stdout = ""
        stderr = "sandbox_apply: Operation not permitted"

    monkeypatch.setattr(seatbelt.shutil, "which", lambda _: "/usr/bin/sandbox-exec")
    monkeypatch.setattr(seatbelt.subprocess, "run", lambda *args, **kwargs: Result())
    assert seatbelt.admitted() == (False, "sandbox_apply: Operation not permitted")
