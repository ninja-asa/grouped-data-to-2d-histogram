import pandas as pd

from pytest import fixture, raises
from unittest.mock import patch, Mock
import tempfile

import os
from datetime import datetime

from histogram2d import orchestrator
from histogram2d.orchestrator import Orchestrator

@fixture
def sample_raw_df() -> pd.DataFrame:
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
def no_groups_sample_raw_df() -> pd.DataFrame:
    data = {
        'Unnamed 1': ["F1", 2, 3, 4, 5],
        'Unnamed 1': ["F2", 2.1, 3.1, 4.1, 5.1],
        'Unnamed 2': ["F3", 2.2, 3.3, 4.4, 5.5],
        'Unnamed B': ["F1", 2, 3, 4, 5],
        'Unnamed 3': ["F2", 2.1, 3.1, 4.1, 5.1],
    }
    df = pd.DataFrame(data)
    return df


@fixture
def sample_groups_dfs()-> list[pd.DataFrame]:
    data = {
        'A': [1, 1, 1, 0, 1],
        'B': [1, 1, 1, -1, 1],
        'C': [1, 1, 1, 0, 1],
    }
    df1 = pd.DataFrame(data)
    data = {
        'A': [2, 2, 3, 4, 5],
        'B': [2, 2, 3, 4, 10],
        'C': [1, 1, 1, 0, 1]
    }
    df2 = pd.DataFrame(data)
    return [df1, df2]

@fixture
def write_sample_csv(sample_raw_df) -> str:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        file_path = temp_file.name
        sample_raw_df.to_csv(file_path, index=False)
        return file_path
@fixture
def write_sample_excel(sample_raw_df) -> str:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        file_path = temp_file.name
        sample_raw_df.to_excel(file_path, index=False)
        return file_path
    
@fixture
def sample_orchestrator():
    # create temporary folder
    with tempfile.TemporaryDirectory() as temp_dir:
        orchestrator = Orchestrator(debug=True, root_folder=temp_dir)
        yield orchestrator

def test_get_sub_dfs(sample_raw_df, sample_orchestrator, no_groups_sample_raw_df):
    groups_df, groups_name = sample_orchestrator.get_groups_df(sample_raw_df)
    assert len(groups_df) == 2
    # Assert first group has three features and 4 data rows
    assert groups_df[0].shape == (4, 3)
    # Assert second group has two features and 4 data rows
    assert groups_df[1].shape == (4, 2)
    # Assert group names are A and B
    assert groups_name == ['A', 'B']
    # Assert column names are F1, F2, F3
    assert groups_df[0].columns.tolist() == ['F1', 'F2', 'F3']
    
    # Test with a dataframe that does not have groups
    groups_df, groups_name = sample_orchestrator.get_groups_df(no_groups_sample_raw_df)
    assert len(groups_df) == 1
    assert groups_name == [""]
    

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


@patch('histogram2d.orchestrator.datetime')
def test_prepare_outputs_folder(mock_datetime, sample_orchestrator):
    # Call the prepare_outputs_folder method
    datetime_now_value = datetime(2021, 1, 1, 12, 0, 0)
    mock_datetime.now.return_value = datetime_now_value
    with tempfile.TemporaryDirectory() as temp_dir:
        outputs_folder = sample_orchestrator.prepare_outputs_folder(temp_dir)

        # Assert that the outputs folder exists
        assert os.path.exists(outputs_folder)

        # Assert that the outputs folder is created with the correct name format
        expected_folder_name = datetime_now_value.strftime("%Y-%m-%d_%H-%M-%S")
        assert outputs_folder.endswith(expected_folder_name)

        # Assert that the outputs folder is created inside the root folder
        assert outputs_folder.startswith(temp_dir)

def test_init(sample_orchestrator):
    # Assert that the orchestrator is created with the correct debug value
    assert sample_orchestrator.debug

    # Assert that the orchestrator is created with the correct root folder
    assert os.path.exists(sample_orchestrator.output_folder)


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

def test_is_data_file_valid(sample_orchestrator, write_sample_csv, write_sample_excel):
    # Test with a valid csv file
    assert sample_orchestrator.is_data_file_valid(write_sample_csv)

    # Test with a valid excel file
    assert sample_orchestrator.is_data_file_valid(write_sample_excel)

    # Test with an invalid file - non existent
    with raises(Exception):
        sample_orchestrator.is_data_file_valid("invalid_file.csv")

    # Test with an invalid file - not a csv or excel file
    with raises(Exception):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            file_path = temp_file.name
            assert not sample_orchestrator.is_data_file_valid(file_path)

def test_read_data_from_file(sample_orchestrator, write_sample_csv, write_sample_excel):
    # Act : Read data from the csv file
    data_of_groups, group_names = sample_orchestrator.read_data_from_file(write_sample_csv)

    # Assert that the dataframe is not empty
    assert len(data_of_groups) == 2
    
    # Assert the correct group names were found
    assert group_names == ['A', 'B'] 

    # Assert that the dataframe has the correct number of rows and columns
    assert data_of_groups[0].shape == (4, 3)

    # Act : Read data from the excel file
    data_of_groups, group_names = sample_orchestrator.read_data_from_file(write_sample_excel)

    # Assert that the dataframe is not empty
    assert len(data_of_groups) == 2
    
    # Assers the correct group names were found
    assert group_names == ['A', 'B']

    # Assert that the dataframe has the correct number of rows and columns
    assert data_of_groups[0].shape == (4, 3)

    # Test with an invalid file
    with raises(Exception):
        sample_orchestrator.read_data_from_file("invalid_file.csv")

def test_get_max_min_column_value(sample_orchestrator, sample_groups_dfs):
    # drop
    # Act : Get the max and min values of the first column
    max_value, min_value = sample_orchestrator.get_max_min_column_value(sample_groups_dfs, "A")

    # Assert that the max value is 5
    assert max_value == 5

    # Assert that the min value is 0
    assert min_value == 0

    # Act : Get the max and min values of the second column
    max_value, min_value = sample_orchestrator.get_max_min_column_value(sample_groups_dfs, "B")

    # Assert that the max value is 10
    assert max_value == 10

    # Assert that the min value is -1
    assert min_value == -1

def test_get_features_ranges(sample_orchestrator, sample_groups_dfs):
    # Act : Get the features ranges
    feature_ranges = sample_orchestrator.get_features_ranges(sample_groups_dfs, ['A', 'B', 'C'])

    # Assert that the feature ranges are correct and only two are shown
    assert feature_ranges == {
        'A': (5, 0),
        'B': (10, -1)
    }

    # Act and Assert : get the features ranges with a feature that does not exist
    with raises(Exception):
        feature_ranges = sample_orchestrator.get_features_ranges(sample_groups_dfs, ['D'])
    

def test_update_settings_with_max_min_feature_1(sample_orchestrator):
    # Act : Update the settings with the min and max values of the first feature
    sample_orchestrator.update_settings_with_max_min_feature_1(1,2)

    # Assert that the settings have been updated correctly
    assert sample_orchestrator.histogram2d_settings.min_feature_1 == 2
    assert sample_orchestrator.histogram2d_settings.max_feature_1 == 1

def test_update_settings_with_max_min_feature_2(sample_orchestrator):
    # Act : Update the settings with the min and max values of the second feature
    sample_orchestrator.update_settings_with_max_min_feature_2(1,2)

    # Assert that the settings have been updated correctly
    assert sample_orchestrator.histogram2d_settings.min_feature_2 == 2
    assert sample_orchestrator.histogram2d_settings.max_feature_2 == 1

def test_update_histogram_settings_based_on_features(sample_orchestrator):
    # Arrange
    features = ['A', 'B']
    feature_ranges = {
        'A': (5, 0),
        'B': (10, -1)
    }

    # Act : Update the histogram settings based on the features
    sample_orchestrator.update_histogram_settings_based_on_features(features, feature_ranges)

    # Assert that the settings have been updated correctly
    assert sample_orchestrator.histogram2d_settings.min_feature_1 == 0
    assert sample_orchestrator.histogram2d_settings.max_feature_1 == 5
    assert sample_orchestrator.histogram2d_settings.min_feature_2 == -1
    assert sample_orchestrator.histogram2d_settings.max_feature_2 == 10
    assert sample_orchestrator.histogram2d_settings.x_axis_title == 'A'
    assert sample_orchestrator.histogram2d_settings.y_axis_title == 'B'


def test_write_image_to_formats(sample_orchestrator):
    # Arrange
    fig = Mock()
    
    title = 'test_title'
    formats = ['pdf', 'svg', 'png']

    # Act
    sample_orchestrator.write_image_to_formats(fig, title, formats)

    # Assert
    fig.write_image.assert_any_call(f"{sample_orchestrator.output_folder}/test_title.pdf")
    fig.write_image.assert_any_call(f"{sample_orchestrator.output_folder}/test_title.svg")
    fig.write_image.assert_any_call(f"{sample_orchestrator.output_folder}/test_title.png")


def test_get_features(sample_orchestrator, sample_groups_dfs):
    # Act: Provide no features selection
    features = sample_orchestrator.get_features(sample_groups_dfs)

    # Assert: Select first two features
    assert features == ['A', 'B']

    # Act: Provide features selection
    features = sample_orchestrator.get_features(sample_groups_dfs, ['A', 'C'])

    # Assert: Select first and third features
    assert features == ['A', 'C']

    # Act: Provide invalid features selection
    with raises(Exception):
        sample_orchestrator.get_features(sample_groups_dfs, ['A', 'D'])
    
    # Arrange
    first_df = sample_groups_dfs[0]
    # get only first column
    first_df = first_df[first_df.columns[0]]
    # Act: Provide no features selection when df has only one column
    with raises(Exception):
        features = sample_orchestrator.get_features([first_df])

