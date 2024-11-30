from pathlib import Path

import pytest

RESOURCES_FOLDER = Path(__file__).parent / "resources"


@pytest.fixture()
def resources() -> Path:
    return RESOURCES_FOLDER.absolute()
