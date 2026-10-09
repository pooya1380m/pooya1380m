"""CLI exposing the tools (also usable as an LLM tool registry via TOOLS)."""
from __future__ import annotations

import argparse
import json

from . import calc, compliance, photometry

TOOLS = {
    "parse_photometry": photometry.load,
    "luminaires_needed": calc.luminaires_needed,
    "check_compliance": compliance.check,
}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="dialux-agent")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("parse"); a.add_argument("file")
    b = sub.add_parser("estimate")
    b.add_argument("--lux", type=float, required=True)
    b.add_argument("--length", type=float, required=True)
    b.add_argument("--width", type=float, required=True)
    b.add_argument("--height", type=float, required=True, help="mounting height above workplane")
    b.add_argument("--flux", type=float, required=True, help="lumens per luminaire")
    b.add_argument("--mf", type=float, default=0.8)
    c = sub.add_parser("check")
    c.add_argument("room"); c.add_argument("--em", type=float, required=True)
    c.add_argument("--u0", type=float, required=True)
    c.add_argument("--ugr", type=float); c.add_argument("--ra", type=float)
    args = p.parse_args(argv)
    if args.cmd == "parse":
        l = photometry.load(args.file)
        print(json.dumps({**l.__dict__, "efficacy_lm_per_w": l.efficacy_lm_per_w}))
    elif args.cmd == "estimate":
        print(calc.luminaires_needed(args.lux, args.length, args.width, args.flux, args.height, args.mf))
    else:
        v = compliance.check(args.room, args.em, args.u0, args.ugr, args.ra)
        print("OK" if not v else "\n".join(v))
        return 1 if v else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
