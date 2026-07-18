"""Interactive CLI: roll batches, keep the bangers, weights retune themselves."""

import argparse
import random

from . import keepers as kp
from .generator import generate_batch

HELP = """\
commands:
  <enter> or r   reroll a new batch
  2 7 ...        keep those names from the batch (numbers, space-separated)
  k              list all keepers
  d <name>       drop a name from the keepers
  s              show keeper-derived weight tuning
  h              this help
  q              quit"""


def _show_batch(batch, number):
    print(f"\n-- batch {number} " + "-" * 28)
    for i, name in enumerate(batch, 1):
        print(f"  {i:2}. {name}")
    print()


def _show_stats():
    keepers = kp.load_keepers()
    counts = kp.feature_counts(keepers)
    print(f"\n{len(keepers)} keepers on file. Pattern counts feeding the weights")
    print(f"(each hit adds +{kp.ALPHA:g} to base weight, capped at {kp.CAP:g}x base):\n")
    for kind in ("onset", "coda", "suffix", "stem"):
        ranked = counts[kind].most_common()
        line = ", ".join(f"{v} x{c}" for v, c in ranked) if ranked else "(none parsed)"
        print(f"  {kind + ':':8} {line}")
    print()


def _keep(batch, indices):
    kept, dupes = [], []
    for i in indices:
        if not 1 <= i <= len(batch):
            print(f"  no #{i} in this batch")
            continue
        name = batch[i - 1]
        (kept if kp.save_keeper(name) else dupes).append(name)
    if kept:
        print("  kept: " + ", ".join(kept))
    if dupes:
        print("  already had: " + ", ".join(dupes))


def interactive(rng, batch_size):
    print("Phonetic Goblin Generator -- enter to reroll, numbers to keep, h for help")
    batch_num = 0

    def new_batch():
        nonlocal batch_num
        batch_num += 1
        # retuned every roll so fresh keeps take effect immediately
        w = kp.tuned_weights()
        return generate_batch(batch_size, rng, w, exclude=kp.load_keepers())

    batch = new_batch()
    _show_batch(batch, batch_num)
    while True:
        try:
            cmd = input("goblin> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        parts = cmd.split()
        if cmd == "" or cmd == "r":
            batch = new_batch()
            _show_batch(batch, batch_num)
        elif all(p.isdigit() for p in parts):
            _keep(batch, [int(p) for p in parts])
        elif cmd == "k":
            names = kp.load_keepers()
            print("\n".join(f"  {n}" for n in names) or "  (no keepers yet)")
        elif parts[0] == "d" and len(parts) > 1:
            name = " ".join(parts[1:])
            print(f"  dropped {name}" if kp.remove_keeper(name)
                  else f"  {name} isn't in the keepers")
        elif cmd == "s":
            _show_stats()
        elif cmd == "h":
            print(HELP)
        elif cmd == "q":
            break
        else:
            print("  ? -- h for help")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="goblins",
                                 description="Generate phonetic goblin names.")
    ap.add_argument("-n", type=int, metavar="N",
                    help="one-shot: print N names and exit (default: interactive)")
    ap.add_argument("-b", "--batch", type=int, default=10,
                    help="interactive batch size (default 10)")
    ap.add_argument("--seed", type=int, help="RNG seed for reproducible rolls")
    args = ap.parse_args(argv)

    rng = random.Random(args.seed)
    if args.n:
        w = kp.tuned_weights()
        print("\n".join(generate_batch(args.n, rng, w,
                                       exclude=kp.load_keepers())))
    else:
        interactive(rng, args.batch)


if __name__ == "__main__":
    main()
