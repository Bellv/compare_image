import unittest

from unittest.mock import call, patch

import numpy as np

from scripts.compare_script import (
    get_page_list,
    page_split,
    threshold_split,
    remove_and_replace_element,
    remove_prefix_and_suffix,
    group_content,
    report,
    generate_difference_report,
    get_fail_list,
    count_report,
    main_process
)


class CompareScriptTest(unittest.TestCase):
    @patch('scripts.compare_script.remove_and_replace_element')
    @patch('scripts.compare_script.open')
    def test_get_page_list_should_get_pages_list_successfully(
        self,
        mock_with_open,
        mock_remove_and_replace_element
        ):

        get_page_list()

        mock_with_open.assert_called_once()
        mock_remove_and_replace_element.assert_called_once()

    def test_page_split_should_get_file_page_name_successfully(self):
        raw_page = 'www.test.com_,'

        result = page_split(raw_page)
        expected = 'www.test.com_.png'
        self.assertEqual(result, expected)

        raw_page = 'www.test.com_,0.044'

        result = page_split(raw_page)
        expected = 'www.test.com_.png'
        self.assertEqual(result, expected)

    def test_threshold_split_should_get_threshold_successfully(self):
        raw_page = 'www.test.com_'

        result = threshold_split(raw_page)
        expected = '0.01'
        self.assertEqual(result, expected) 

        raw_page = 'www.test.com_,0.02'

        result = threshold_split(raw_page)
        expected = '0.02'
        self.assertEqual(result, expected)

    def test_remove_and_replace_element_should_replace_successfully(self):
        content_list = [
            'http://test', 'https://test2', 'test3\n', '\ntest4', 'test5/'
        ]

        result = remove_and_replace_element(content_list)
        expected = ['test', 'test2', 'test3', 'test4', 'test5_']
        self.assertEqual(result, expected)

    def test_remove_prefix_and_suffix_should_remove_successfully(self):
        content_list = [
            'test1',
            'Blink-Diff test',
            'Copyright test',
            'Clipping test',
            'Images test',
            'Wrote test',
            'Time test',
            'test2',
        ]

        result = remove_prefix_and_suffix(content_list)
        expected = ['test1', 'test2']
        self.assertEqual(result, expected)

    def test_group_content_should_grouped_successfully(self):
        content_list = ['test1', 'test2', 'FAIL', 'test4', 'test5', 'FAIL']

        result = group_content(content_list)
        expected = np.array(content_list).reshape(2,3)
        self.assertIn(result, expected)

        content_list = ['test1', 'test2', 'FAIL', 'test4', 'test5', 'FAIL',
                        'test1', 'test2', 'FAIL', 'test4', 'test5', 'FAIL']

        result = group_content(content_list)
        expected = np.array(content_list).reshape(4,3)
        self.assertIn(result, expected)

    def test_report_should_return_fail_page_successfully(self):
        content_grouped = [['test1', 'test2', 'PASS']]

        result = report(content_grouped)
        expected = None
        self.assertEqual(result, expected)

        content_grouped = [['test1', 'test2', 'FAIL']]

        result = report(content_grouped)
        expected = 'test1 - test2'
        self.assertEqual(result, expected)

    @patch('scripts.compare_script.report')
    @patch('scripts.compare_script.group_content')
    @patch('scripts.compare_script.remove_prefix_and_suffix')
    @patch('scripts.compare_script.remove_and_replace_element')
    @patch('scripts.compare_script.open')
    @patch('scripts.compare_script.os.system')
    def test_generate_difference_report_should_return_fail_list_successfully(
        self, 
        mock_os_system,
        mock_with_open,
        mock_remove_and_replace_element,
        mock_remove_prefix_and_suffix,
        mock_group_content,
        mock_report
        ):

        page = 'www.test.com_.png'
        threshold = '0.02'

        result = generate_difference_report(page, threshold)

        mock_os_system.assert_called_once()
        mock_with_open.assert_called_once()
        mock_remove_and_replace_element.assert_called_once()
        mock_remove_prefix_and_suffix.assert_called_once()
        mock_group_content.assert_called_once()
        mock_report.assert_called_once()

    @patch('scripts.compare_script.generate_difference_report')
    @patch('scripts.compare_script.threshold_split')
    @patch('scripts.compare_script.page_split')
    def test_get_fail_list_should_return_fail_list_successfully(
        self,
        mock_page_split,
        mock_threshold_split,
        mock_generate_difference_report
        ):

        pages = ['www.test.com_', 'www.test.com_,0.02']

        get_fail_list(pages)

        call_page_split = []
        call_threshold_split = []

        for raw_page in pages:
            call_page_split.append(call(raw_page))
            call_threshold_split.append(call(raw_page))
            mock_generate_difference_report.assert_called()

    def test_count_report_should_return_count_number_successfully(self):
        fail_list = [None, None, None]
        
        result = count_report(fail_list)
        expected = [3, 0, []]
        self.assertEqual(result, expected)

        fail_list = ['www.test.com_.png - Differences: 162400 (4.45%)']
        
        result = count_report(fail_list)
        expected = [1, 1, ['www.test.com_.png - Differences: 162400 (4.45%)']]
        self.assertEqual(result, expected)
        
        fail_list = [
            None, None, 'www.test.com_.png - Differences: 162400 (4.45%)'
        ]
        
        result = count_report(fail_list)
        expected = [3, 1, ['www.test.com_.png - Differences: 162400 (4.45%)']]
        self.assertEqual(result, expected)

    @patch('scripts.compare_script.os.remove')
    @patch('scripts.compare_script.count_report')
    @patch('scripts.compare_script.get_fail_list')
    @patch('scripts.compare_script.get_page_list')
    def test_main_process_should_run_all_process_successfully(
        self,
        mock_get_page_list,
        mock_get_fail_list,
        mock_count_report,
        mock_os_remove
        ):

        main_process()

        mock_get_page_list.assert_called_once_with()
        mock_get_fail_list.assert_called_once()
        mock_count_report.assert_called_once()
        mock_os_remove.assert_called_once()


if __name__ == '__main__':
    unittest.main()

