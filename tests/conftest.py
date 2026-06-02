from __future__ import annotations

from pathlib import Path

import pytest

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


@pytest.fixture
def hpa_path() -> Path:
    return EXAMPLES / "hpa-axis.yaml"
