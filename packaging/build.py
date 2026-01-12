#!/usr/bin/env python3
"""Build helper for PyInstaller."""
from __future__ import annotations

import argparse
from pathlib import Path

import PyInstaller.__main__


DEFAULT_ENTRY = Path("src/main.py")
DEFAULT_SPEC = Path("packaging/pyinstaller.spec")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the app with PyInstaller.")
    parser.add_argument(
        "--entry",
        type=Path,
        default=DEFAULT_ENTRY,
        help="Entry script to package (default: src/main.py).",
    )
    parser.add_argument(
        "--name",
        default="YoloApp",
        help="Application name (default: YoloApp).",
    )
    parser.add_argument(
        "--onefile",
        action="store_true",
        help="Build a single-file executable.",
    )
    parser.add_argument(
        "--windowed",
        action="store_true",
        help="Do not open a console window (GUI apps).",
    )
    parser.add_argument(
        "--spec",
        type=Path,
        default=DEFAULT_SPEC,
        help="Path to PyInstaller spec file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spec_path = args.spec

    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    cli_args = [str(spec_path), f"--name={args.name}"]
    if args.onefile:
        cli_args.append("--onefile")
    if args.windowed:
        cli_args.append("--windowed")
    cli_args.append(f"--paths={args.entry.parent}")
    cli_args.append(f"--specpath={spec_path.parent}")
    cli_args.append(f"--workpath=build/{args.name}")
    cli_args.append(f"--distpath=dist/{args.name}")

    PyInstaller.__main__.run(cli_args)


if __name__ == "__main__":
    main()
