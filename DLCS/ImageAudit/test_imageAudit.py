import pytest
from imageAudit import *
import pandas as pd

script_dir = os.path.dirname(__file__)

#tests for list diff
def test_list_diff_1():
    L1 = [1,2,3]
    L2 = [1,'X',3]
    output = list_diff(L1,L2)
    assert output == [2]

def test_list_diff_2():
    L1 = [1,2,3]
    L2 = [1,'X',3]
    output = list_diff(L2,L1)
    assert output == ['X']

#tests for merged lists
def test_merge_csv_extra():
    csv_list = ['file_1', 'file_2']
    disk_list = ['file_1']
    out_dicts = [{'File Name': 'file_1',
                  'On disk': True,
                  'On CSV': True},
                 {'File Name': 'file_2',
                  'On disk': False,
                  'On CSV': True}]
    assert get_merged_lists(csv_list, disk_list, script_dir) == out_dicts

def test_merge_disk_extra():
    csv_list = ['file_1']
    disk_list = ['file_1','file_3']
    out_dicts = [{'File Name': 'file_1',
                  'On disk': True,
                  'On CSV': True},
                 {'File Name': 'file_3',
                  'On disk': True,
                  'On CSV': False}]
    assert get_merged_lists(csv_list, disk_list, script_dir) == out_dicts
    
def test_merge_identical():
    csv_list = ['file_1']
    disk_list = ['file_1']
    out_dicts = [{'File Name': 'file_1',
                  'On disk': True,
                  'On CSV': True}]
    assert get_merged_lists(csv_list, disk_list, script_dir) == out_dicts

def test_csv_writing():
	test_path = os.path.join(script_dir, 'Test Materials', 'test_export.csv')
	expected_path = os.path.join(script_dir, 'Test Materials', 'test_export_expected.csv')
	test_csv = pd.read_csv(test_path)
	expected_csv = pd.read_csv(expected_path)
	assert test_csv.equals(expected_csv)