
import os
import sys
import datetime
import colorama
import argparse

class File:

    _DATETIME_STR_FORMAT = '%Y-%m-%dT%H:%m:%S'

    def __init__(self, file_name, epoch_mtime, epoch_ctime):
        self.file_name = file_name
        self.epoch_mtime = epoch_mtime
        self.epoch_ctime = epoch_ctime

    @property
    def modification_datetime_obj(self):
        return datetime.datetime.fromtimestamp(self.epoch_mtime)

    @property
    def creation_datetime_obj(self):
        return datetime.datetime.fromtimestamp(self.epoch_ctime)

    @property
    def modification_datetime_iso_str(self):
        return self.modification_datetime_obj.strftime(self._DATETIME_STR_FORMAT)

    @property
    def creation_datetime_iso_str(self):
        return self.creation_datetime_obj.strftime(self._DATETIME_STR_FORMAT)

    def __lt__(self, other):
        '''
        The lower than verification will be based on the files modification time value
        '''
        return self.epoch_mtime < other.epoch_mtime

def get_latest_files(top_limit=None, max_depth=None, source_dir='.'):
    found_files = list()
    for dirpath, _, files in os.walk(source_dir, followlinks=True):
        no_of_dirs = dirpath.replace(source_dir, '').split(os.sep)

        if max_depth:
            if len(no_of_dirs) > max_depth:
                break

        for file in files:
            file_name = dirpath + os.sep + file
            stat = os.stat(file_name)
            f = File(file_name, stat.st_mtime, stat.st_ctime)
            found_files.append(f)

    result = sorted(found_files, reverse=True)
    if top_limit:
        return result[:top_limit]
    else:
        return result


def print_header(modification_dt_str):
    print('{}Modification datetime:{} {} {}'.format(
        colorama.Fore.GREEN, 
        colorama.Fore.BLUE, 
        modification_dt_str, 
        colorama.Style.RESET_ALL)
    )


def main(sys_args=sys.argv[1:]):
    args = arg_parser.parse_args(sys_args)
    colorama.init()

    top_limit = args.max_files if args.max_files else None
    max_depth = args.max_depth if args.max_depth else None

    found_files = get_latest_files(top_limit=top_limit, max_depth=max_depth, source_dir=args.search_dir)
    last_modification_dt_str = ''
    for f in found_files:
        modification_dt_str = f.modification_datetime_iso_str
        if last_modification_dt_str != modification_dt_str:
            last_modification_dt_str = modification_dt_str
            if not args.file_names_only:
                print_header(modification_dt_str)

        before_file_name = '\t\t' if not args.file_names_only else ''

        print('{}{}{}{}{}'.format(before_file_name, colorama.Style.BRIGHT,
                                  colorama.Fore.YELLOW, f.file_name, colorama.Style.RESET_ALL))


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--file-names-only', '-n',
                        help='Indicates the output on the screen should include the file names only', action='store_true')
arg_parser.add_argument(
    '--max-files', '-m', help='Indicates the max number of files to be reported in the output, from the most recent to the last', type=int)
arg_parser.add_argument(
    '--max-depth', '-d', help='Indicates the depth level for the search to be done, considering the level of subfolders in the search directory', type=int)
arg_parser.add_argument(
    'search_dir', help='The directory from which the search has to start', default='.', const='.', nargs='?')

if __name__ == '__main__':
    main(sys.argv[1:])
