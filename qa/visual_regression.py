"""Simple pixel-diff utility for visual regression tests."""
from __future__ import annotations

from pathlib import Path
import click
from PIL import Image, ImageChops


@click.command()
@click.argument("baseline", type=click.Path(exists=True, path_type=Path))
@click.argument("candidate", type=click.Path(exists=True, path_type=Path))
@click.option("--threshold", default=0.02, help="Allowed percentage delta before failing.")
def compare(baseline: Path, candidate: Path, threshold: float) -> None:
    base = Image.open(baseline).convert("RGB")
    cand = Image.open(candidate).convert("RGB")
    if base.size != cand.size:
        raise click.ClickException("Images must share identical dimensions")

    diff = ImageChops.difference(base, cand)
    histogram = diff.histogram()
    total_pixels = base.size[0] * base.size[1] * 3
    diff_pixels = sum(value for idx, value in enumerate(histogram) if idx % 256 != 0)
    ratio = diff_pixels / total_pixels

    click.echo(f"Pixel delta: {ratio:.4%}")
    if ratio > threshold:
        raise click.ClickException(
            f"Pixel delta {ratio:.2%} exceeds threshold {threshold:.2%}")


if __name__ == "__main__":
    compare()
