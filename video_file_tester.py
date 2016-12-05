import os
import file_item
import errno
import unittest

class FileInputTesting(unittest.TestCase):
    def test1(self):
        self.assertRaises(FileNotFoundError,
                          file_item.video_file,
                          '~/dne')
    def test2(self):
        try:
            file_item.video_file('~/Movies/class_video_test/MVI_4299.MOV')
        except FileNotFoundError:
            self.fail('file_item.video_file() raised FileNotFoundError ' +
                      'unexpectedly')
    def test3(self):
        try:
            file_item.video_file('/Users/elliots/Movies/class_video_test/'+
                                 'MVI_4299.MOV')
        except FileNotFoundError:
            self.fail('file_item.video_file() raised FileNotFoundError ' +
                      'unexpectedly')

if __name__ == '__main__':
    unittest.main()
