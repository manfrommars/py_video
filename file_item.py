# Container for video files
import os

class video_file(object):
    def __init__(self, filepath):
        # Verify the file exists
        if not os.path.exists(filepath):
            raise Exception('Filepath does not exist %s' % filepath)
        # Gather available data about the file
