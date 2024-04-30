from histogram2d.orchestrator import Orchestrator
from histogram2d.histogram2d import Histogram2DContourSettings
from histogram2d.visualize import VisualizeSettings

# CHANGE BELOW CONFIGURATIONS TO CUSTOMIZE THE VISUALIZATION
excel_file = "data/dummy.xlsx" # "dummy.xlsx "# "AreavsIntensity.xlsx"
DEBUG = False
features = [
    "Area", 
    "Intensity"
    ] # Expected to be two strings, matching the feature names in the excel file. If empty, the first two features will be used.

# GROUP NAMES WILL BE AUTODISCOVERED FROM THE EXCEL FILE
settings_histogram = Histogram2DContourSettings(
    min_feature_1=None, # set to None to auto calculate minimum value of feature 1 in the provided data
    max_feature_1=None, # set to None to auto calculate maximum value of feature 1 in the provided data
    min_feature_2=None, # set to None to auto calculate minimum value of feature 2 in the provided data
    max_feature_2=None, # set to None to auto calculate maximum value of feature 2 in the provided data
    feature_1_bin_size=25000, # set to None to auto calculate bin size of feature 1 in the provided data #TODO: validate this
    feature_2_bin_size=0.01, # set to None to auto calculate bin size of feature 2 in the provided data #TODO: validate this
    hist_colorbar_min=0, # set to None to auto calculate minimum value of the colorbar in the provided data #TODO: validate this
    hist_colorbar_max=7, # set to None to auto calculate maximum value of the colorbar in the provided data #TODO: validate this
    colorscale="viridis", # check https://plotly.com/python/builtin-colorscales/
    contours=dict(
        showlabels=True, # show number of counts/percentage in each contour of the histogram
        labelfont=dict(color="black") # set the color of the labels
        ),
    contour_filling="fill", # set to "fill" to fill the contours with color, set to "lines" to show only the lines of the contours
    contour_show_lines=False, # set to True to show the lines of the contours
    normalized=True, # set to True to show the percentage of counts in each contour, set to False to show the count of each contour
)

settings_multiplot = VisualizeSettings(
    horizontal_spacing=0.08, # set the horizontal spacing between subplots
    vertical_spacing=0.15, # set the vertical spacing between subplots
    fig_suplots_width=1600, # set the width of the figure
    fig_subplot_height_per_row=800, # set the height of the figure
)

def main() -> None:
    runner = Orchestrator(
        histogram2d_settings=settings_histogram,
        multiplot_settings=settings_multiplot,
        debug=True,
    )
    runner.run(excel_filepath=excel_file)


if __name__ == "__main__":
    main()
