import argparse
import json
import os
import sys
import tempfile

from galaxy.files import ConfiguredFileSources


def get_file_sources(file_sources_path):
    assert os.path.exists(file_sources_path), "file sources path [%s] does not exist" % file_sources_path
    with open(file_sources_path, "r") as f:
        file_sources_as_dict = json.load(f)
    file_sources = ConfiguredFileSources.from_dict(file_sources_as_dict)
    return file_sources


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = _parser().parse_args(argv)
    file_sources = get_file_sources(args.file_sources)
    directory_uri = args.directory_uri
    counter = 0
    for real_data_path, name in zip(args.infiles, args.names):
        if directory_uri.endswith("/"):
            target_uri = directory_uri + name
        else:
            target_uri = directory_uri + "/" + name
        file_source_path = file_sources.get_file_source_path(target_uri)
        if os.path.exists(file_source_path.path):
            print(f'Error: File "{file_source_path.path}" already exists. Aborting.')
        file_source = file_source_path.file_source
        file_source.write_from(file_source_path.path, real_data_path)
        counter += 1
    print(f'In total {counter} files have been exported.\n')


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory_uri', type=str,
                        help='directory target URI')
    parser.add_argument('--file_sources', type=str, help='file sources json')
    parser.add_argument('--infiles', type=str, nargs='*', required=True)
    parser.add_argument('--names', type=str, nargs='*', required=True)
    return parser


if __name__ == "__main__":
    main()
