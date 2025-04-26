import os
import sys
import shutil
from argparse import ArgumentParser
from tempfile import TemporaryDirectory

from cyan import tbhutils, tbhtypes


def main(parser: ArgumentParser) -> None:
  args = parser.parse_args()
  args.i = os.path.normpath(args.input)

  if args.output is not None:
    args.o = os.path.normpath(args.output)
    if not (
        args.o.endswith(".app")
        or args.o.endswith(".ipa")
        or args.o.endswith(".tipa")
    ):
      print("[?] valid file extension not found; will create ipa")
      args.o += ".ipa"
  else:
    args.o = args.i

  # this also modifies some args, like -f,
  # to ensure there are no duplicates, etc
  arg_err = tbhutils.validate_inputs(args)
  if arg_err is not None:
    parser.error(arg_err)

  # mfw when "True if True else False" HAHAHAH
  INPUT_IS_IPA = args.i.endswith(".ipa") or args.i.endswith(".tipa")
  OUTPUT_IS_IPA = args.o.endswith(".ipa") or args.o.endswith(".tipa")

  with TemporaryDirectory() as tmpdir, tbhtypes.LeavingCM():
    app_path = tbhutils.get_app(args.i, tmpdir, INPUT_IS_IPA)
    app = tbhtypes.AppBundle(app_path)

    if app.executable.is_encrypted():
      if args.ignore_encrypted:
        print("[?] main binary is encrypted, ignoring")
      else:
        sys.exit("[!] main binary is encrypted; exiting")

    if args.cyan is not None:
      changing = vars(args)
      tbhutils.parse_cyans(changing, tmpdir)

    # this goes before injection,
    # since user might inject their own extensions
    if args.remove_extensions:
      app.remove_all_extensions()
    elif args.remove_encrypted:
      app.remove_encrypted_extensions()

    if args.f is not None:
      app.executable.inject(args.f, tmpdir)
    if args.n is not None:
      app.plist.change_name(args.n)
    if args.v is not None:
      app.plist.change_version(args.v)
    if args.b is not None:
      app.plist.change_bundle_id(args.b)
    if args.m is not None:
      app.plist.change_minimum_version(args.m)
    if args.k is not None:
      app.change_icon(args.k, tmpdir)
    if args.l is not None:
      app.plist.merge_plist(args.l)
    if args.x is not None:
      app.executable.merge_entitlements(args.x)

    if args.remove_supported_devices:
      app.plist.remove_uisd()
    if args.no_watch:
      app.remove_watch_apps()
    if args.enable_documents:
      app.plist.enable_documents()
    if args.fakesign:
      app.fakesign_all()
    if args.thin:
      app.thin_all()
    if args.substrate_only:
      app.executable.common = {
        "substrate.": {
          "name": "CydiaSubstrate.framework",
          "path": "@rpath/CydiaSubstrate.framework/CydiaSubstrate"
        }
      }

    # create subdirectories if necessary
    if "/" in args.o:
        os.makedirs(os.path.dirname(args.o), exist_ok=True)

    # done !
    if OUTPUT_IS_IPA:
      print(f"[*] generating ipa with compression level {args.compress}..")
      tbhutils.make_ipa(tmpdir, os.path.realpath(args.o), args.compress)
      print(f"[*] generated ipa at {args.o}")
    else:
      if os.path.isdir(args.o):
        shutil.rmtree(args.o)

      shutil.move(app.path, args.o)
      print(f"[*] generated app at {args.o}")

