import copy
import json
import logging
import os

from .sdesk_file import SdeskFile


SDESK_INPUT_PATH = os.environ.get("SDESK_INPUT_PATH", "/input")
SDESK_SUPPLEMENT_PATH = os.environ.get("SDESK_SUPPLEMENT_PATH", "/code")
SDESK_INPUT_METADATA_PATH = f"{SDESK_INPUT_PATH}/input_metadata.json"
SDESK_SAMPLE_INPUT_METADATA_PATH = f"{SDESK_INPUT_PATH}/sample_input_metadata.json"
SDESK_INPUT_PARAMETERS_PATH = f"{SDESK_INPUT_PATH}/input_parameters.json"

SDESK_OUTPUT_PATH = os.environ.get("SDESK_OUTPUT_PATH", "/output")
SDESK_OUTPUT_METADATA_PATH = f"{SDESK_OUTPUT_PATH}/input_metadata_updated.json"
SDESK_OUTPUT_SAMPLE_METADATA_PATH = f"{SDESK_OUTPUT_PATH}/input_samples_meta_updated.json"
SDESK_SUPPORT_FILE_METADATA_PATH = f"{SDESK_SUPPLEMENT_PATH}/support_file_metadata.json"


def get_input_metadata() -> dict:
    try:
        with open(SDESK_INPUT_METADATA_PATH) as file:
            rv = json.load(file)
            return rv
    except:
        return []


def get_sample_input_metadata() -> dict:
    try:
        with open(SDESK_SAMPLE_INPUT_METADATA_PATH) as file:
            rv = json.load(file)
            return rv
    except:
        return []

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


def update_sample_input_metadata(meta_data) -> dict:
    logging.info(f"updating input_metadata")

    out_meta = SdeskFile(SDESK_OUTPUT_SAMPLE_METADATA_PATH)
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
        if pre_header:
            lines = pre_header.split("\n")
            pre_header = "\n".join(["# " + line for line in lines]) + "\n\n"
            fp.write(pre_header)
            fileposition += len(pre_header)

        # Header
        column_names = ["[{0}]".format(col.replace("\n", " ")) for col in columns]
        column_line = "\t".join(column_names) + "\n"
        fp.write(column_line)
        fileposition += len(column_line)
        # Data
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


class DataLoader:
    def __init__(self):
        self.files = []
        self.samples = []
        self.files_metadata = get_input_metadata()
        for i in self.files_metadata:
            self.files.append(InputData(i, 'file', self))

        self.samples_metadata = get_sample_input_metadata()
        for i in self.samples_metadata:
            self.samples.append(InputData(i, 'sample', self))

    def file_commit(self):
        update_input_metadata(self.files_metadata)

    def sample_commit(self):
        update_sample_input_metadata(self.samples_metadata)


class InputData:
    def __init__(self, metadata, data_type, manager):
        self.type = data_type
        self._manager = manager
        self.metadata = metadata
        self.custom_properties = metadata['custom_metadata']
        self.properties = metadata
        if self.type == 'file':
            path = f"{SDESK_INPUT_PATH}/{metadata['actual_name']}"
            self._file = SdeskFile(path)

    @property
    def path(self):
        if self.type == 'file':
            return self._file.path()
        return None

    @property
    def sample(self):
        if not self.metadata.get('sample', False):
            return None
        return InputData(self.metadata['sample'], 'file.sample', self._manager)

    def update_custom_properties(self, data):
        self.metadata['custom_metadata'].update(data)
        self.custom_properties = self.metadata['custom_metadata']
        if self.type == 'sample':
            self._manager.sample_commit()
        if self.type == 'file' or type == 'file.sample':
            self._manager.file_commit()
