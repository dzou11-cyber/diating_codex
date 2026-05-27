"""Calibration utilities for TERS blink analysis.

This module stores stable fitting functions so event analysis code can reuse
the same calibration behavior across sessions.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple


@dataclass(frozen=True)
class StmAsu6Params:
    offset: float = 0.0
    a1: float = -3.1443
    b1: float = -34.3577
    c1: float = -3.611e-11
    d1: float = -2.304e-12
    a2: float = 3.1223
    b2: float = -34.2769
    c2: float = 3.789e-11
    d2: float = -7.791e-12


STM_ASU6 = StmAsu6Params()


@dataclass(frozen=True)
class RamanCubicParams:
    a: float
    b: float
    c: float
    d: float


# Current project default:
# 633nm_2200
RAMAN_633_2200 = RamanCubicParams(
    a=3.28563129e-07,
    b=-1.66014380e-03,
    c=5.29857975e00,
    d=-1.21365471e02,
)


def current_from_sv(sv: float, p: StmAsu6Params = STM_ASU6) -> float:
    """Convert source voltage to current using stm_asu6 fitting."""
    if sv - p.offset >= 0:
        return abs(math.exp(p.a2 * sv + p.b2) + p.c2 * sv + p.d2)
    return -abs(math.exp(p.a1 * sv + p.b1) + p.c1 * sv + p.d1)


def get_current(sv: float, p: StmAsu6Params = STM_ASU6) -> float:
    """Compatibility alias matching existing project code naming."""
    return current_from_sv(sv, p)


def get_G(current: float, bv: float) -> float:
    """Convert current to conductance in G/G0-like scaling."""
    denom = 1e-5 if bv == 0 else bv
    return abs(current * 12900 / denom)


def get_log_G(current: float, bv: float) -> float:
    """Return log10 conductance."""
    return math.log10(get_G(current, bv))


def pixel_to_wavenumber(pixel: float, p: RamanCubicParams = RAMAN_633_2200) -> float:
    """Map CCD pixel to Raman shift (cm^-1) with cubic fitting."""
    return p.a * pixel**3 + p.b * pixel**2 + p.c * pixel + p.d


def trans_y_func(pixel: float, p: RamanCubicParams = RAMAN_633_2200) -> int:
    """Integer Raman-axis transform for plotting ticks."""
    return int(pixel_to_wavenumber(pixel, p))


def residuals(pixel: float, target_y: float, p: RamanCubicParams = RAMAN_633_2200) -> float:
    """Residual between fitted Raman shift and target value."""
    return pixel_to_wavenumber(pixel, p) - target_y


def generate_raman_axis(num_pixels: int = 1024, p: RamanCubicParams = RAMAN_633_2200) -> List[int]:
    """Generate integer Raman axis for all pixels."""
    return [int(pixel_to_wavenumber(x, p)) for x in range(num_pixels)]


def detect_num_pixels_from_file(raman_file_path: str | Path) -> int:
    """Infer pixel count from one Raman CSV row (time + pixels)."""
    with Path(raman_file_path).open("r", newline="") as f:
        reader = csv.reader(f)
        first = next(reader)
    if len(first) < 2:
        raise ValueError("Raman file appears empty or malformed.")
    return len(first) - 1


def get_raman_para(raman_file_path: str | Path) -> Tuple[float, float, float, float, List[int]]:
    """Compatibility helper matching your existing workflow.

    For current project data, always returns 633nm_2200 parameters.
    """
    n_pixels = detect_num_pixels_from_file(raman_file_path)
    axis = generate_raman_axis(num_pixels=n_pixels, p=RAMAN_633_2200)
    p = RAMAN_633_2200
    return p.a, p.b, p.c, p.d, axis


if __name__ == "__main__":
    # Minimal self-check
    demo_sv = 0.01
    demo_i = current_from_sv(demo_sv)
    print("Func loading done!")
    print(f"sv={demo_sv}, current={demo_i:.6e}, logG@0.5V={get_log_G(demo_i, 0.5):.6f}")
