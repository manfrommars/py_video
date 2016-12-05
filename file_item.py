# Container for video files
import os
import errno

class video_file(object):
    def __init__(self, filepath):
        # Clean up the filepath
        filepath = os.path.expanduser(filepath)
        # Verify the file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    filepath)
        # Gather available data about the file
