"""
Algorithm example that splits input files in two output files.
"""
import pytest
import json

# sdesk.proc.io package has helpers to read input data and produce output files.
from sdesk.proc import io


def write_file(fname, data):
    with open(fname, "w+") as output_file:
        output_file.writelines(data)


def main():
    # Input metadata is a list of metadata (dict) for every input file.
    input_metadata = io.get_input_metadata()

    # Read the input parameters: this data can be unique to every execution
    # of the algorithm and will be provided by the user uppon exection.
    input_parameters = io.get_input_parameters()
    num_of_lines = int(input_parameters["number_of_lines"])
    print(f"Splitting into {num_of_lines}")

    for in_file in io.get_input_files(input_metadata):
        print(f"Opening file {in_file.path()}")
        with open(in_file.path()) as fp:
            lines = fp.readlines()

            # Split the files in N files of num_of_lines size.
            out = []
            N = num_of_lines
            num_splits = len(lines) // num_of_lines
            for S in range(num_splits):
                out.append(lines[S * N : S * N + N])

            # Put the residual in the last split
            res = len(lines) % num_of_lines
            out[-1].extend(lines[-res:])

            # Create the output files. The files will be collected by ScienceDesk
            # after the algorithm finishes, and registred in the system as a
            # derived files from the input.
            for i, data in enumerate(out):
                out_file = io.create_output_file(in_file.name() + f"-{i}")
                write_file(out_file.path(), data)


@pytest.mark.skip(reason="Unknown")
def test_split():
    main()
