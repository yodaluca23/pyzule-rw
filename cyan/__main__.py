#!/usr/bin/env python3
# cyan, aka pyzule-rw; by zx, 2024

import sys
import argparse


def main() -> None:
  if sys.platform == "win32":
    sys.exit("[!] windows is not supported")

  parser = argparse.ArgumentParser(
    description="cyan, an azule \"clone\" for modifying iOS apps"
  )

  parser.add_argument(
    "-i", "--input", metavar="input", required=True,
    help="the app to be modified (.app/.ipa)"
  )
  parser.add_argument(
    "-o", "--output", metavar="output",
    help="if unspecified, overwrites input"
  )

  parser.add_argument(
    "-z", "--cyan", metavar="cyan", nargs="+",
    help="the .cyan file(s) to use"
  )
  parser.add_argument(
    "-f", metavar="file", nargs="+",
    help="a tweak to inject/item to be added to the bundle"
  )

  parser.add_argument(
    "-n", metavar="name",
    help="modify the app's name"
  )
  parser.add_argument(
    "-v", metavar="version",
    help="modify the app's version"
  )
  parser.add_argument(
    "-b", metavar="bundle id",
    help="modify the app's bundle id"
  )
  parser.add_argument(
    "-m", metavar="minimum",
    help="modify the app's minimum OS version"
  )
  parser.add_argument(
    "-k", metavar="icon",
    help="modify the app's icon"
  )
  parser.add_argument(
    "-l", metavar="plist",
    help="a plist to merge with the app's Info.plist"
  )
  parser.add_argument(
    "-x", metavar="entitlements",
    help="add or modify entitlements to the main binary"
  )

  parser.add_argument(
    "-u", "--remove-supported-devices", action="store_true",
    help="remove UISupportedDevices"
  )
  parser.add_argument(
    "-w", "--no-watch", action="store_true",
    help="remove all watch apps"
  )
  parser.add_argument(
    "-d", "--enable-documents", action="store_true",
    help="enable documents support"
  )
  parser.add_argument(
    "-s", "--fakesign", action="store_true",
    help="fakesign all binaries for use with appsync/trollstore"
  )
  parser.add_argument(
    "-q", "--thin", action="store_true",
    help="thin all binaries to arm64, may largely reduce size"
  )
  parser.add_argument(
    "-e", "--remove-extensions", action="store_true",
    help="remove all app extensions"
  )
  parser.add_argument(
    "-g", "--remove-encrypted", action="store_true",
    help="only remove encrypted app extensions"
  )
  parser.add_argument(
    "-j", "--substrate-only", action="store_true",
    help="only auto-inject substrate (CydiaSubstrate.framework) if needed"
  )

  parser.add_argument(
    "-c", "--compress", metavar="level", type=int, default=6,
    help="the compression level of the ipa (0-9, defaults to 6)",
    action="store", choices=range(0, 10)
  )
  parser.add_argument(
    "--ignore-encrypted", action="store_true",
    help="skip main binary encryption check"
  )
  parser.add_argument(
    "--overwrite", action="store_true",
    help="overwrite existing files without confirming"
  )

  parser.add_argument(
    "--version", action="version", version="cyan v1.4.4"
  )

  from cyan import logic
  logic.main(parser)


if __name__ == "__main__":
  main()

