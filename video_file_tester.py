import os
import file_item
import errno
import unittest
import datetime

class FileInputTesting(unittest.TestCase):
    def test1(self):
        # File does not exist, should raise a FileNotFoundError
        self.assertRaises(FileNotFoundError,
                          file_item.video_file,
                          '~/dne')
    def test2(self):
        # File exists, verify user expansion works for input
        try:
            file_item.video_file('~/Movies/class_video_test/MVI_4299.MOV')
        except FileNotFoundError:
            self.fail('file_item.video_file() raised FileNotFoundError ' +
                      'unexpectedly')
    def test3(self):
        # File exists, verify absolute path works for input
        try:
            test_file = file_item.video_file('/Users/elliots/Movies/'+
                                             'class_video_test/'+
                                             'MVI_4299.MOV')
            self.assertEqual(test_file.get_creation_time(), None)
        except FileNotFoundError:
            self.fail('file_item.video_file() raised FileNotFoundError ' +
                      'unexpectedly')
    def test4(self):
        # File exists, verify datetime is set from file name, not MP4
        # metadata
        try:
            test_file = file_item.video_file('~/Movies/dance_tutorials/' +
                                          'spain_videos_miguel/' +
                                          'VID_20150330_221716.mp4')
            self.assertEqual(test_file.get_creation_time(),
                             datetime.datetime(2015,3,30,22,17,16))
        except FileNotFoundError:
            self.fail('file_item.video_file() raised FileNotFoundError ' +
                      'unexpectedly')
    def test5(self):
        # Verify all files in the folder correctly load
        test_path = os.path.expanduser('~/Movies/dance_tutorials/'+
                                       'spain_videos_miguel/')
        for f in os.listdir(test_path):
            if os.path.isfile(os.path.join(test_path, f)):
                try:
                    file_item.video_file(os.path.join(test_path, f))
                except FileNotFoundError:
                    self.fail('file_item.video_file() raised '+
                              'FileNotFoundError unexpectedly')
    def test6(self):
        # File exists, verify relative path works for input
        try:
            test_file = file_item.video_file('../../Movies/'+
                                             'class_video_test/'+
                                             'MVI_4299.MOV')
            self.assertEqual(test_file.get_creation_time(), None)
        except FileNotFoundError:
            self.fail('file_item.video_file() raised FileNotFoundError ' +
                      'unexpectedly')        

if __name__ == '__main__':
    unittest.main()
    
