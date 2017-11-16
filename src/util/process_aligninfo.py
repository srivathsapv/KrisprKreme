import argparse  # module that passes command-line arguments into script


def main(**kwargs):
    # check if already args is provided, i.e. main() is called from the top level script
    args = kwargs.get('args', None)
    if args is None:  ## i.e. standalone script called from command line in normal way
        parser = argparse.ArgumentParser(description="Parse SAM file to get alignment details")
        parser._optionals.title = "Arguments"
        parser.add_argument("-i", "--infile", help="""Infile (required)""", type=str, metavar="<file.txt>",
                            required=True)
        parser.add_argument("-o", "--out_file", help="""Output file (required)""", type=str, metavar="<file.txt>",
                            required=False)

        args = parser.parse_args()

    infile = args.infile




if __name__ == "__main__":
    main()
