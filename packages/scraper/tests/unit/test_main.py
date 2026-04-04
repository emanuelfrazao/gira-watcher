"""Group 11: CLI entrypoint -- argparse validation."""

import subprocess
import sys

import pytest


def test_help_exits_cleanly() -> None:
    """11.1: `python -m scraper.main --help` exits with code 0."""
    result = subprocess.run(
        [sys.executable, "-m", "scraper.main", "--help"],
        capture_output=True,
        text=True,
        cwd=None,
    )
    assert result.returncode == 0
    assert "--run-type" in result.stdout


def test_valid_run_type_is_accepted() -> None:
    """11.2: --run-type station is accepted by argparse."""
    from scraper.main import _parse_args

    args = _parse_args(["--run-type", "station"])
    assert args.run_type == "station"


def test_invalid_run_type_raises_system_exit() -> None:
    """11.3: --run-type invalid raises SystemExit with code 2."""
    from scraper.main import _parse_args

    with pytest.raises(SystemExit) as exc_info:
        _parse_args(["--run-type", "invalid"])
    assert exc_info.value.code == 2
