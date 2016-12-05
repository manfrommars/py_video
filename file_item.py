# Container for video files
# Standard Python libraries
import os
import errno
import datetime
import hashlib
# Custom Python libraries
from mp4_parser import mp4_parser
import filename_parser

# A video_file has a filepath, creation time (or best guess), a file hash
# (to verify if the file changes), last modification date, and dictionary of
# tags
class video_file(object):
    def __init__(self, filepath):
        # Clean up the filepath
        self.filepath = os.path.expanduser(filepath)
        # Verify the file exists
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    self.filepath)
        filename = os.path.basename(self.filepath)
        # Gather available data about the file
        # For MP4 files, check for the creation date in the file
        metadata_info = None
        if os.path.splitext(filename)[-1].lower() == '.mp4':
            creation_secs = mp4_parser.findMp4Field(self.filepath,
                                                    'creation_time')
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
        self.file_hash = self.get_md5sum(self.filepath)
    def get_md5sum(self, filepath):
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    def get_creation_time(self):
        return self.creation_time
    def get_hash(self):
        return self.file_hash
