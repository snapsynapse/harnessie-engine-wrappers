import platform
import os

import pytest

from harnessie_engine_wrappers.probe import run_probe
from harnessie_engine_wrappers.seatbelt import admitted


@pytest.mark.skipif(platform.system() != "Darwin", reason="macOS Seatbelt probe")
def test_live_reference_probe_passes():
    backend_ok, detail = admitted()
    if not backend_ok and os.environ.get("HEW_REQUIRE_LIVE_PROBE") != "1":
        pytest.skip(f"Seatbelt unavailable in this process context: {detail}")
    assert backend_ok, detail
    result = run_probe()
    assert result["ok"] is True, result
    assert all(result["checks"].values())
