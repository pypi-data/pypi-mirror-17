Generate and run a tkinter GUI for an argparse.ArgumentParser object.

Usage:
python -m geniegui myprogram

Here myprogram must be a Python module that has two functions:

1. get_argument_parser() -- returning an ArgumentParser object p
2. main() -- the main function calling p = get_argument_parser() and setting args = p.parse_args()