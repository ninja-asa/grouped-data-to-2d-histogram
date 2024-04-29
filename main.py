from orchestrator import Orchestrator
from histogram2d import Histogram2DContourSettings
from visualize import VisualizeSettings

excel_file = 'AreavsIntensity.xlsx'
AREA_COLUMN_NAME = 'Area'
INTENSITY_COLUMN_NAME = 'Intensity'
DEBUG = False

settings_histogram = Histogram2DContourSettings(
    min_area=None, 
    max_area=None, 
    min_intensity=None, 
    max_intensity=None,
    area_bin_size=25000,
    intensity_bin_size=0.01,
    count_min=0,
    count_max=7,
    colorscale='viridis',
    contours = dict(
        showlabels = True,
        labelfont = dict(
            color = 'black'
        )
    ),    
    contour_filling = 'fill',
    contour_show_lines = False,
    normalized = True
)

settings_multiplot = VisualizeSettings(
    horizontal_spacing=0.08,
    vertical_spacing=0.15,
    fig_suplots_width = 1600,
    fig_subplot_height = 800
)

titles = [
    "Flat",
    "1 µm",
    "2 µm",
    "3 µm",
    "4 µm",
    "5 µm"
]

def main() -> None:
    runner = Orchestrator(
        histogram2d_settings=settings_histogram,
        multiplot_settings=settings_multiplot,
        debug=False
    )
    runner.run(
        excel_filepath=excel_file,
        titles=titles
    )

if __name__ == "__main__":
    main()