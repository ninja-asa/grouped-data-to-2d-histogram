from histogram2d.builder import Histogram2DContourSettings
from histogram2d.visualize import VisualizeSettings

# Setting Configurable Parameters to None - Auto Calculation of params per Histogram

settings_histogram = Histogram2DContourSettings(
    min_feature_1=None,  # set to None to auto calculate minimum value of feature 1 in the provided data
    max_feature_1=None,  # set to None to auto calculate maximum value of feature 1 in the provided data
    min_feature_2=None,  # set to None to auto calculate minimum value of feature 2 in the provided data
    max_feature_2=None,  # set to None to auto calculate maximum value of feature 2 in the provided data
    feature_1_bin_size=25000,  # set to None to auto calculate bin size of feature 1 in the provided data #TODO: validate this
    feature_2_bin_size=0.01, #0.01,  # set to None to auto calculate bin size of feature 2 in the provided data #TODO: validate this
    hist_colorbar_min=0,  # set to None to auto calculate minimum value of the colorbar in the provided data #TODO: validate this
    hist_colorbar_max=7,# 7,  # set to None to auto calculate maximum value of the colorbar in the provided data #TODO: validate this
    colorscale="greens",  # check https://plotly.com/python/builtin-colorscales/
    contours=dict(
        showlabels=True,  # show number of counts/percentage in each contour of the histogram
        labelfont=dict(color="black"),  # set the color of the labels
    ),
    contour_filling="fill",  # set to "fill" to fill the contours with color, set to "lines" to show only the lines of the contours
    contour_show_lines=False,  # set to True to show the lines of the contours
    normalized=False,  # set to True to show the percentage of counts in each contour, set to False to show the count of each contour
)
