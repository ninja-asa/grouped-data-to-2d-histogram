from unittest.mock import Mock, patch
import pytest
import pandas as pd
from plotly.graph_objects import Histogram2dContour
from histogram2d.builder import Histogram2DContourSettings

@pytest.fixture()
def sample_histogram_settings() -> Histogram2DContourSettings:
    return Histogram2DContourSettings()

def test_get_z_colorbar_label(sample_histogram_settings):
    sample_histogram_settings.normalized = True
    assert sample_histogram_settings.get_z_colorbar_label() == "Percentage"

    sample_histogram_settings.normalized = False
    assert sample_histogram_settings.get_z_colorbar_label() == "Count"

def test_create_histogram2dcontour_normalized():
    # Arrange
    histogram = Histogram2DContourSettings()
    histogram.create_frequency_histogram2dcontour = Mock()
    histogram.create_count_histogram2dcontour = Mock()
    histogram.normalized = True
    df = pd.DataFrame()  # replace with actual DataFrame if needed

    # Act
    histogram.create_histogram2dcontour(df)

    # Assert
    histogram.create_frequency_histogram2dcontour.assert_called_once_with(df)
    histogram.create_count_histogram2dcontour.assert_not_called()

def test_create_histogram2dcontour_not_normalized():
    # Arrange
    histogram = Histogram2DContourSettings()
    histogram.create_frequency_histogram2dcontour = Mock()
    histogram.create_count_histogram2dcontour = Mock()
    histogram.normalized = False
    df = pd.DataFrame()  # replace with actual DataFrame if needed

    # Act
    histogram.create_histogram2dcontour(df)

    # Assert
    histogram.create_frequency_histogram2dcontour.assert_not_called()
    histogram.create_count_histogram2dcontour.assert_called_once_with(df)

def test_create_count_histogram2dcontour(sample_histogram_settings):
    # Arrange
    sample_histogram_settings.x_axis_title = "x"
    sample_histogram_settings.y_axis_title = "y"
    df = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y": [4, 5, 6]
        }
    )  # replace with actual DataFrame if needed

    # Act
    result = sample_histogram_settings.create_count_histogram2dcontour(df)

    # Assert
    assert result is not None  # add more specific checks if needed
    assert isinstance(result, Histogram2dContour)