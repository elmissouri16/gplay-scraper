import os
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_WHEEL_DIR = Path("/usr/share/python-wheels")


def _install_to_target(target_dir: Path) -> None:
    """Install the project into a target directory without network/deps."""
    # Ensure pip exists for the current interpreter (some uv envs omit it).
    subprocess.run(
        [sys.executable, "-m", "ensurepip", "--upgrade"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Ensure setuptools/wheel are present so the build backend is available.
    missing_build = []
    for module in ("setuptools", "wheel"):
        try:
            __import__(module)
        except ModuleNotFoundError:
            missing_build.append(module)

    if missing_build:
        base_cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
        ]

        def try_install(extra_args: list[str]) -> bool:
            result = subprocess.run(
                base_cmd + extra_args + missing_build,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PIP_NO_CACHE_DIR": "1", "PIP_DISABLE_PIP_VERSION_CHECK": "1"},
            )
            return result.returncode == 0

        # Prefer offline system wheel cache if present; fall back to index if needed.
        tried = False
        if SYSTEM_WHEEL_DIR.exists():
            tried = True
            if try_install(["--no-index", f"--find-links={SYSTEM_WHEEL_DIR}"]):
                missing_build = []
        if missing_build:
            tried = True
            if try_install([]):
                missing_build = []

        if missing_build:
            import pytest

            pytest.skip(
                f"Missing build tooling ({', '.join(missing_build)}) and installation failed "
                f"(tried_offline={'yes' if tried else 'no'})."
            )

    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--no-cache-dir",
        "--no-deps",
        "--no-build-isolation",
        "--target",
        str(target_dir),
        str(PROJECT_ROOT),
    ]
    result = subprocess.run(
        cmd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "PIP_NO_CACHE_DIR": "1", "PIP_DISABLE_PIP_VERSION_CHECK": "1"},
    )
    if result.returncode != 0:
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise AssertionError(
            f"pip install failed with code {result.returncode}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        )


def test_packaging_includes_subpackages():
    """Ensure packaged install contains nested modules like gplay_scraper.core."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "site-packages"
        _install_to_target(target)

        sys.path.insert(0, str(target))
        try:
            from gplay_scraper import GPlayScraper  # type: ignore
            from gplay_scraper.core import gplay_methods  # type: ignore

            assert GPlayScraper is not None
            assert hasattr(gplay_methods, "AppMethods")
        finally:
            sys.path.pop(0)
