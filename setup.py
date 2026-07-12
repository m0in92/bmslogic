"""Setuptools build hooks for BMSLogic."""

from pathlib import Path
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py


class CMakeBuildPy(build_py):
    """Build CMake extension modules before copying Python packages."""

    def run(self):
        source_dir = Path(__file__).resolve().parent
        build_dir = source_dir / "build"
        build_dir.mkdir(exist_ok=True)

        subprocess.check_call(["cmake", ".."], cwd=build_dir)
        subprocess.check_call(["cmake", "--build", "."], cwd=build_dir)

        super().run()


setup(cmdclass={"build_py": CMakeBuildPy})