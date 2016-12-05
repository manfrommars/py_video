# Container for video files
# Standard Python libraries
import os
import errno
import datetime
# Custom Python libraries
from mp4_parser import mp4_parser
import filename_parser

class video_file(object):
    def __init__(self, filepath):
        # Clean up the filepath
        filepath = os.path.expanduser(filepath)
        # Verify the file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    filepath)
        filename = os.path.basename(filepath)
        # Gather available data about the file
        # For MP4 files, check for the creation date in the file
        metadata_info = None
        if os.path.splitext(filename)[-1].lower() == '.mp4':
            creation_secs = mp4_parser.findMp4Field(filepath, 'creation_time')
            metadata_info = datetime.datetime(1901, 1, 1)
            metadata_info += datetime.timedelta(seconds=creation_secs)
        file_dt = filename_parser.datetimeFromFilename(filename)
        if file_dt == datetime.datetime(1900, 1, 1, 0, 0, 0):
            if metadata_info:
                self.creation_time = metadata_info
            else:
                self.creation_time = None
        else:
            self.creation_time = file_dt
    def get_creation_time(self):
        return self.creation_time
