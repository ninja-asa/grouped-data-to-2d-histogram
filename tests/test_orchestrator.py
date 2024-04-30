import pandas as pd

from pytest import fixture
from unittest.mock import patch

import os
from datetime import datetime

from src.orchestrator import Orchestrator

@fixture
def sample_df() -> pd.DataFrame:
    data = {
        'A': ["F1", 2, 3, 4, 5],
        'Unnamed 1': ["F2", 2.1, 3.1, 4.1, 5.1],
        'Unnamed 2': ["F3", 2.2, 3.3, 4.4, 5.5],
        'B': ["F1", 2, 3, 4, 5],
        'Unnamed 3': ["F2", 2.1, 3.1, 4.1, 5.1],
    }
    df = pd.DataFrame(data)
    return df

@fixture
def sample_orchestrator() -> Orchestrator:
    return Orchestrator(debug=True)

def test_get_sub_dfs(sample_df, sample_orchestrator):
    groups_df, groups_name = sample_orchestrator.get_groups_df(sample_df)
    assert len(groups_df) == 2
    # Assert first group has three features and 4 data rows
    assert groups_df[0].shape == (4, 3)
    # Assert second group has two features and 4 data rows
    assert groups_df[1].shape == (4, 2)
    # Assert group names are A and B
    assert groups_name == ['A', 'B']
    # Assert column names are F1, F2, F3
    assert groups_df[0].columns.tolist() == ['F1', 'F2', 'F3']
    

def test_cleanup_group_df(sample_orchestrator):
    # Create a sample dataframe
    data = {
        'A': ["F1", 2, 3, 4, 5],
        'B': ["F1", 2, 3, 4, 5],
        'C': ["F1", 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)

    # Call the cleanup_group_df method
    cleaned_df = sample_orchestrator.cleanup_group_df(df)

    # Assert that the first row is removed
    assert len(cleaned_df) == len(df) - 1

    # Assert column names are F1, and not A, B, C
    assert cleaned_df.columns.tolist() == ['F1']*3


@patch('src.orchestrator.datetime')
def test_prepare_outputs_folder(mock_datetime, sample_orchestrator):
    # Call the prepare_outputs_folder method
    datetime_now_value = datetime(2021, 1, 1, 12, 0, 0)
    mock_datetime.now.return_value = datetime_now_value

    outputs_folder = sample_orchestrator.prepare_outputs_folder()

    # Assert that the outputs folder exists
    assert os.path.exists(outputs_folder)

    # Assert that the outputs folder is created with the correct name format
    expected_folder_name = datetime_now_value.strftime("%Y-%m-%d_%H-%M-%S")
    assert outputs_folder.endswith(expected_folder_name)

    # Cleanup the folder
    os.rmdir(outputs_folder)


def test_is_group_column_name(sample_orchestrator):
    # Test with a column name that contains "unnamed" substring
    column_name = "Unnamed 1"
    assert not sample_orchestrator.is_group_column_name(column_name)

    # Test with a column name that does not contain "unnamed" substring
    column_name = "A"
    assert sample_orchestrator.is_group_column_name(column_name)

    # Test with a column name that contains "unnamed" substring in different case
    column_name = "UNNAMED : 2"
    assert not sample_orchestrator.is_group_column_name(column_name)

    # Test with a column name that contains "unnamed" substring as a part of another word
    column_name = "unnamEd_3"
    assert not sample_orchestrator.is_group_column_name(column_name)

