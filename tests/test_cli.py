import json

from harnessie_engine_wrappers import cli


def test_unsupported_platform_refuses_before_command(monkeypatch, capsys):
    monkeypatch.setattr(cli.platform, "system", lambda: "Linux")
    assert cli.main(["--", "true"]) == 69
    refusal = json.loads(capsys.readouterr().err)
    assert refusal["error"] == "platform_unsupported"
    assert "why" in refusal


def test_broad_policy_refuses(monkeypatch, capsys):
    monkeypatch.setattr(cli, "DEFAULT_CREDENTIAL_PATHS", ())
    assert cli.main(["--deny", "/", "--", "true"]) == 64
    assert json.loads(capsys.readouterr().err)["error"] == "invalid_policy"
