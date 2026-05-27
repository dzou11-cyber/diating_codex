import argparse
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ters_calibration import get_current, get_log_G, pixel_to_wavenumber


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cond", required=True, help="Path to conductance CSV")
    parser.add_argument("--raman", required=True, help="Path to Raman CSV")
    parser.add_argument("--t0", type=float, required=True, help="Window start (s)")
    parser.add_argument("--t1", type=float, required=True, help="Window end (s)")
    parser.add_argument("--out", required=True, help="Output PNG path")
    args = parser.parse_args()

    t0, t1 = args.t0, args.t1

    ct, sv, bv, pv = [], [], [], []
    with Path(args.cond).open("r", newline="") as f:
        r = csv.reader(f)
        for row in r:
            t = float(row[0])
            if t0 <= t <= t1:
                ct.append(t)
                sv.append(float(row[1]))
                bv.append(float(row[2]))
                pv.append(float(row[3]))

    ct = np.array(ct)
    sv = np.array(sv)
    bv = np.array(bv)
    pv = np.array(pv)
    current = np.array([get_current(x) for x in sv])
    logg = np.array([get_log_G(i, b) for i, b in zip(current, bv)])

    rt, spec = [], []
    with Path(args.raman).open("r", newline="") as f:
        r = csv.reader(f)
        for row in r:
            t = float(row[0])
            if t0 <= t <= t1:
                rt.append(t)
                spec.append([float(x) for x in row[1:]])

    rt = np.array(rt)
    spec = np.array(spec)
    pix = np.arange(spec.shape[1])
    shift = pixel_to_wavenumber(pix)

    vmin = float(np.percentile(spec, 2))
    vmax = float(np.percentile(spec, 99.5))

    fig = plt.figure(figsize=(10, 6), dpi=150)
    gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.02)

    ax0 = fig.add_subplot(gs[0, 0])
    im = ax0.pcolormesh(rt, shift, spec.T, shading="auto", cmap="turbo", vmin=vmin, vmax=vmax)
    ax0.set_ylabel("Raman Shift / cm$^{-1}$")
    ax0.set_xlim(t0, t1)
    ax0.tick_params(axis="x", labelbottom=False)
    cbar = fig.colorbar(im, ax=ax0, orientation="horizontal", pad=0.05, fraction=0.05)
    cbar.set_label("Intensity (a.u.)")

    ax1 = fig.add_subplot(gs[1, 0], sharex=ax0)
    ax1.plot(ct, logg, color="0.25", lw=1.2)
    ax1.axhline(-2, color="0.6", ls=":", lw=0.8, label="Log(G/G0) = -2")
    ax1.set_ylabel("Conductance / log_G")
    ax1.set_xlabel("Time / s")
    ax1.grid(alpha=0.25)
    ax1.legend(loc="upper right", fontsize=8)

    ax2 = ax1.twinx()
    ax2.plot(ct, pv, color="blue", alpha=0.45, lw=1.0)
    ax2.set_ylabel("Piezo Voltage / V", color="blue")
    ax2.tick_params(axis="y", colors="blue")

    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 45))
    ax3.plot(ct, bv, color="red", alpha=0.45, lw=1.0)
    ax3.set_ylabel("Bias Voltage / V", color="red")
    ax3.tick_params(axis="y", colors="red")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight")
    print(out)


if __name__ == "__main__":
    main()
