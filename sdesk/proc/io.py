import copy
import json
import logging
import os

from .sdesk_file import SdeskFile


SDESK_INPUT_PATH = os.environ.get("SDESK_INPUT_PATH", "/input")
SDESK_SUPPLEMENT_PATH = os.environ.get("SDESK_SUPPLEMENT_PATH", "/code")
SDESK_INPUT_METADATA_PATH = f"{SDESK_INPUT_PATH}/input_metadata.json"
SDESK_INPUT_PARAMETERS_PATH = f"{SDESK_INPUT_PATH}/input_parameters.json"

SDESK_OUTPUT_PATH = os.environ.get("SDESK_OUTPUT_PATH", "/output")
SDESK_OUTPUT_METADATA_PATH = f"{SDESK_OUTPUT_PATH}/input_metadata_updated.json"

SDESK_SUPPORT_FILE_METADATA_PATH = f"{SDESK_SUPPLEMENT_PATH}/support_file_metadata.json"


def get_input_metadata() -> dict:
    with open(SDESK_INPUT_METADATA_PATH) as file:
        rv = json.load(file)
        return rv


def get_input_parameters() -> dict:
    with open(SDESK_INPUT_PARAMETERS_PATH) as file:
        rv = json.load(file)
        return rv


def get_input_files(input_metadata):
    input_files = []
    for in_file in input_metadata:
        path = f"{SDESK_INPUT_PATH}/{in_file['actual_name']}"
        input_files.append(SdeskFile(path))
    return input_files


def update_input_metadata(meta_data) -> dict:
    logging.info(f"updating input_metadata")

    out_meta = SdeskFile(SDESK_OUTPUT_METADATA_PATH)
    logging.debug(f"input_metadata path: {out_meta.path()}")

    with open(out_meta.path(), "w+") as f:
        json.dump(meta_data, f)
    return out_meta


def create_output_file(name, meta={}) -> SdeskFile:
    fname = f"{SDESK_OUTPUT_PATH}/{name}"
    return SdeskFile(fname, meta)


def force_str(object):
    try:
        return str(object)
    except:
        pass
    try:
        return object.encode("utf-8")
    except:
        pass
    try:
        return object.encode("utf-8", "ignore").decode("utf-8")
    except:
        pass
    try:
        return object.encode("ascii", "ignore").decode("ascii")
    except:
        return ""


def write_tsv_file(file_path, columns, data, pre_header=""):
    with open(file_path, "w") as fp:
        fileposition = 0
        # Header
        column_names = [col.replace("\n", " ") for col in columns]
        column_line = "\t".join(column_names) + "\n"
        fp.write(column_line)
        fileposition += len(column_line)
        # Data
        if pre_header:
            fp.write(pre_header)
            fileposition += len(pre_header)

        for row in data:
            strings = [force_str(elem) for elem in row]
            data_line = "\t".join(strings) + "\n"
            fp.write(data_line)
            fileposition += len(data_line)

    return fileposition


def get_support_files_metadata() -> dict:
    with open(SDESK_SUPPORT_FILE_METADATA_PATH) as file:
        rv = json.load(file)
        return rv


def get_support_files(suppor_files_metadata):
    support_files = []
    for in_file in suppor_files_metadata:
        path = f"{SDESK_SUPPLEMENT_PATH}/{in_file['actual_name']}"
        support_files.append(SdeskFile(path))
    return support_files
