import glob
import os
import re

import matplotlib.pyplot as plt
import numpy
import numpy as np


class EndoFiles:

    def __init__(self, path: str, prefix: str = 'Raw-*', suffix: str = '-*.npy'):
        self.all_files = None
        self.selected_files = None
        self.path = path
        self.prefix = prefix
        self.suffix = suffix
        self.selected_days = None
        self.times_between = None
        self.get(path = self.path)

    def get(self, path: str = '') -> list[str]:
        if path:
            self.path = path
        search_expr = os.path.join(self.path, self.prefix + self.suffix)
        self.all_files = glob.glob(search_expr)
        return self.all_files

    def filter_days(self, days: list[str]) -> list[str]:
        if self.selected_files is not None:
            filtered_list = np.array(self.selected_files)
        else:
            filtered_list = np.array(self.all_files)
        filter_idx = []

        for i in range(0, len(filtered_list) - 1):
            info = self.get_file_info_from_name(filtered_list[i])
            day = info[1]
            if day not in days:
                filter_idx.append(i)

        self.selected_days = days
        self.selected_files = np.delete(filtered_list, filter_idx)
        return self.selected_files

    def filter_times(self, between: list[str]) -> list[str]:
        if not between:
            start = int(0)
            stop = int(999999)
        else:
            _start = int(between[0])
            _stop = int(between[1])
            if _start > _stop:
                start = _stop
                stop = _start
            else:
                start = _start
                stop = _stop

        if self.selected_files is not None:
            filtered_list = np.array(self.selected_files)
        else:
            filtered_list = np.array(self.all_files)

        filter_idx = []

        for i in range(0, len(filtered_list) - 1):
            info = self.get_file_info_from_name(filtered_list[i])
            timestamp = int(info[2])
            if timestamp not in range(start, stop):
                filter_idx.append(i)

        self.times_between = between
        self.selected_files = np.delete(filtered_list, filter_idx)
        return self.selected_files

    @staticmethod
    def get_file_info_from_name(
            filepath: str,
            regexp: str = r"(\w+)-(\d{4}\d{2}\d{2})-(\d{6})-(\d{3}).(\w*)",
            display: bool = False,
    ) -> tuple[str]:
        filepath = os.path.basename(filepath)
        matches = re.match(regexp, filepath)

        if display:
            if matches:
                print("Match object: %s" % (matches))
                if matches.groups():
                    for i in range(0, matches.lastindex + 1):
                        print("Group %s: %s" % (i, matches.group(i)))

        return matches.groups()

    def __str__(self):
        is_selected = self.selected_files is not None
        is_days_filter = self.selected_days is not None
        is_times_filter = self.times_between is not None

        str = f"""
           Active path: {self.path}
           Total files found in path: {len(self.all_files)}
           Number of selected files: {len(self.selected_files) if is_selected else len(self.all_files)}
           Selected days: {self.selected_days if is_days_filter else None}
           Times between: {self.times_between if is_times_filter else None}
        """

        return str

    def __repr__(self):
        pass



class EndoRawData:
    def __init__(self, filepath):
        self.filepath = filepath
        self.rawdata = self.read()

    def read(self) -> dict[str, numpy.ndarray]:
        try:
            # Read as numpy.ndarray of size ()
            self.rawdata = np.load(self.filepath, allow_pickle=True)
            self.rawdata = self.rawdata.item()
            # Return as dict
            return self.rawdata
        except:
            return None

    @property
    def start_time(self):
        return self.rawdata['tstart']

    @property
    def timestamp(self):
        return self.rawdata['tstamp']

    def info(self) -> None:
        print("Available keys: %s" % (self.rawdata.keys()))
        print("Start timestamp: %s" % self.start_time)
        print("Timestamp: %s" % self.timestamp)

    def check_channel(self, channel: str = 'PMT1') -> bool:
        if self.rawdata[channel] is not None:
            return True
        else:
            return False

    def plot_channel(self, channel: str = 'PMT1'):
        if self.check_channel(channel=channel):
            plt.figure()
            plt.plot(self.rawdata[channel])



if __name__ == "__main__":
    fs = EndoFiles(
        path='C:/Users/jerem/Downloads/tufts_20221114/raw_G202207-06_obj=2100um4fps/'
    )
    li = fs.filter_days(days=['20221114'])
    li = fs.filter_times(between=['231200', '231400'])
    print(fs)


