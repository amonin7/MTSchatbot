import unittest
import os
from DataServiceFile import IDataService, TextDataService
import datetime


class TestTextDataService(unittest.TestCase):

    def __clean_tmp_file(self, fname):
        if os.path.exists(fname):
            os.remove(fname)

    def __init_test(self):
        file_path = 'test_tmp.txt'
        self.__clean_tmp_file(file_path)
        t = TextDataService(file_path)
        return file_path, t

    def __is_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def __is_datetime(self, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            return True
        except ValueError:
            return False

    def test_TextDataService_SaveNormalMessage_ShouldSaveMessageInFile(self):

        file_path, t = self.__init_test()

        t.save_message("test message", "test answer", 1)
        with open(t.text_file_path, "rt") as f:
            text = f.read()

        self.assertNotEqual(text, "")
        self.assertNotEqual(text, None)
        os.remove(file_path)

    def test_TextDataService_SaveMessageIdInCorrectFormat_ShouldBeClientIDTimeClientMessageAnswer(self):

        file_path, t = self.__init_test()

        message = "test message"
        answer = "test answer"
        clinent_id = 1

        t.save_message(message, answer, clinent_id)
        with open(t.text_file_path, "rt") as f:
            line = f.readline()

        saved_id, save_time, save_message, saved_answer = line.split("\t")[:-1]

        self.assertTrue(self.__is_int(saved_id))
        self.assertTrue(self.__is_datetime(save_time))
        self.assertTrue(isinstance(saved_answer, str))
        self.assertTrue(isinstance(save_message, str))

        os.remove(file_path)

    def test_TextDataService_SaveMessageCorrectSaving_ShouldSaveIdCurrentTimeMessageAndAnswer(self):
        pass


if __name__ == '__main__':
    unittest.main()