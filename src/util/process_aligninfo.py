import argparse #module that passes command-line arguments into script
import io

def main(**kwargs):

    #check if already args is provided, i.e. main() is called from the top level script
    args = kwargs.get('args', None)
    if args is None: ## i.e. standalone script called from command line in normal way
        parser = argparse.ArgumentParser(description = "Parse SAM file to get alignment details")
        parser._optionals.title = "Arguments"
        parser.add_argument("-i","--infile", help = """Infile (required)""", type=str, metavar = "<file.txt>", required=True)
        parser.add_argument("-o","--out_file", help = """Output file (required)""", type = str, metavar = "<file.txt>", required=False)

        args = parser.parse_args()

    infile=args.infile

    match_list = []
    align_info=[]

    with open(infile, 'r') as query:
        for line in query:
            line=line.rstrip()

            #Get each line delimited by tab 
            if line.startswith('@'):
                continue
            else:
                line=line.split("\t")

                #Get the reference seq name from 3rd column, offset from 4th column and edit transcript  from the 6th column
                refseq_name=line[2]
                offset=line[3]
                edit_transcript=line[5]

                align_info.append(refseq_name)
                align_info.append(offset)
                align_info.append(edit_transcript)

                #Add to match list
                match_list.append(align_info)
                align_info=[]


    for match in match_list:
        print(match)

if __name__ == "__main__":
    main()
