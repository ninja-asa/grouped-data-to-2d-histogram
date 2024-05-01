import os
import shutil

from histogram2d.visualize import VisualizeSettings
from histogram2d.orchestrator import Orchestrator

from configAuto import settings_histogram as settings_histogram_auto
from configNormalized import settings_histogram as settings_histogram_normalized
from configCount import settings_histogram as settings_histogram_count

excel_file = f"{os.path.dirname(os.path.abspath(__file__))}/dummy.csv"  # "dummy.xlsx "# "AreavsIntensity.xlsx"
DEBUG = False
features = []

settings_multiplot = VisualizeSettings(
    horizontal_spacing=0.08,  # set the horizontal spacing between subplots
    vertical_spacing=0.15,  # set the vertical spacing between subplots
    fig_suplots_width=1600,  # set the width of the figure
    fig_subplot_height_per_row=800,  # set the height of the figure
)

def move_png_files_to_dir(from_dir, to_dir):  
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    for file in os.listdir(from_dir):
        if file.endswith(".png"):
            shutil.copy(os.path.join(from_dir, file), os.path.join(to_dir))

def main() -> None:
    module_dir = os.path.dirname(os.path.abspath(__file__))

    runner = Orchestrator(
        histogram2d_settings=settings_histogram_auto,
        multiplot_settings=settings_multiplot,
        debug=DEBUG,
    )
    runner.run(excel_filepath=excel_file)
    output_folder = runner.output_folder
    target_dir = os.path.join(module_dir, "auto")
    move_png_files_to_dir(output_folder, target_dir)

    runner = Orchestrator(
        histogram2d_settings=settings_histogram_normalized,
        multiplot_settings=settings_multiplot,
        debug=DEBUG,
    )
    runner.run(excel_filepath=excel_file)
    output_folder = runner.output_folder
    target_dir = os.path.join(module_dir, "normalized")
    move_png_files_to_dir(output_folder, target_dir)

    runner = Orchestrator(
        histogram2d_settings=settings_histogram_count,
        multiplot_settings=settings_multiplot,
        debug=DEBUG,
    )
    runner.run(excel_filepath=excel_file)
    output_folder = runner.output_folder
    target_dir = os.path.join(module_dir, "count")
    move_png_files_to_dir(output_folder, target_dir)
    
if __name__ == "__main__":
    main()

