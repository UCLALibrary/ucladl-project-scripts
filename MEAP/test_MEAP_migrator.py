import pytest
import MEAP_migrator
import pandas as pd
import os

script_dir = os.path.dirname(__file__)

def test_full_csv():
    test_input_path = os.path.join(script_dir, 'Test Materials', 'MEAP_test_input.csv')
    MEAP_migrator.main(test_input_path)

    test_output_path = os.path.join(script_dir, 'MEAP_output.csv')
    test_expected_path = os.path.join(script_dir, 'Test Materials', 'MEAP_output_expected.csv')

    expected_csv = pd.read_csv(test_expected_path)
    actual_csv = pd.read_csv(test_output_path)

    assert actual_csv.equals(expected_csv)
