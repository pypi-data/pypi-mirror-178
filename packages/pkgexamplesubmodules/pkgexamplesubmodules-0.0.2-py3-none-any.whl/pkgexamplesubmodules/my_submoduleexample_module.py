import argparse
from rexsubmodule1.src.rexsubmodule1.sayhello import SayHello as SM1_SayHello
from .rexsubmodule2.src.rexsubmodule2.sayhello import SayHello as SM2_SayHello


def my_submodule():
    sub1_sayhello = SM1_SayHello()
    sub2_sayhello = SM2_SayHello()
    main_group_parser = argparse.ArgumentParser(
        description="A submodule package usage example."
    )

    main_group_parser.add_argument(
        "-o",
        "--subone",
        action="store_true",
        help="Submodule one will say hello.",
    )

    main_group_parser.add_argument(
        "-t",
        "--subtwo",
        action="store_true",
        help="Submodule two will say hello.",
    )

    my_args = main_group_parser.parse_args()

    if my_args.subone:
        sub1_sayhello.sayhello()

    if my_args.subtwo:
        sub2_sayhello.sayhello()
