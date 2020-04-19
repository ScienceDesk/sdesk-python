import copy
import json
import logging
import os

from .sdesk_file import SdeskFile


SDESK_INPUT_PATH = os.environ.get("SDESK_INPUT_PATH", "/input")
SDESK_INPUT_METADATA_PATH = f"{SDESK_INPUT_PATH}/input_metadata.json"
SDESK_INPUT_PARAMETERS_PATH = f"{SDESK_INPUT_PATH}/input_parameters.json"

SDESK_OUTPUT_PATH = os.environ.get("SDESK_OUTPUT_PATH", "/output")
SDESK_OUTPUT_METADATA_PATH = f"{SDESK_OUTPUT_PATH}/input_metadata.json"


def get_input_metadata() -> dict:
    with open(SDESK_INPUT_METADATA_PATH) as file:
        rv = json.load(file)
        print(rv)
        return rv


def get_input_parameters() -> dict:
    with open(SDESK_INPUT_PARAMETERS_PATH) as file:
        rv = json.load(file)
        print(rv)
        return rv

def get_input_files(input_metadata):
    input_files = []
    for in_file in input_metadata:
        path = f"{SDESK_INPUT_PATH}/{in_file['path']}"
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
