from plotly.subplots import make_subplots
from plotly.graph_objects import Figure
import pandas as pd
from histogram2d import Histogram2DContourSettings
from dataclasses import dataclass

@dataclass
class VisualizeSettings(object):
    horizontal_spacing: float = 0.08
    vertical_spacing: float = 0.15
    fig_suplots_width: int = 1600
    fig_subplot_height: int = 800
    

    def build_multiplots_figure(
            self,
            dataframes: list[pd.DataFrame], 
            titles: list[str],
            settings_histogram: Histogram2DContourSettings) -> Figure:
        
        fig = make_subplots(
            rows=2, 
            cols=3,
            subplot_titles=titles,
            horizontal_spacing=self.horizontal_spacing,
            vertical_spacing=self.vertical_spacing,
            specs=[
                [{"type": "histogram2dcontour"}, {"type": "histogram2dcontour"}, {"type": "histogram2dcontour"}],
                [{"type": "histogram2dcontour"}, {"type": "histogram2dcontour"}, {"type": "histogram2dcontour"}]
            ],
            column_widths=[1, 1, 1],
            row_heights=[1, 1]
        )


        fig.add_trace(
            settings_histogram.create_histogram2dcontour(
                df = dataframes[0]), 
            row=1, col=1
        )

        fig.add_trace(
            settings_histogram.create_histogram2dcontour(
                df = dataframes[1],), 
            row=1, col=2
        )

        fig.add_trace(
            settings_histogram.create_histogram2dcontour(
                df = dataframes[2]), 
            row=1, col=3
        )

        fig.add_trace(
            settings_histogram.create_histogram2dcontour(
                df = dataframes[3]), 
            row=2, col=1
        )

        fig.add_trace(
            settings_histogram.create_histogram2dcontour(
                df = dataframes[4]), 
            row=2, col=2
        )

        fig.add_trace(
            settings_histogram.create_histogram2dcontour(
                df = dataframes[5]), 
            row=2, col=3
        )

        fig.update_traces(contours_coloring=settings_histogram.contour_filling, 
                        contours_showlines=settings_histogram.contour_show_lines)
            # set size of plot
        fig.update_layout(
            width=self.fig_suplots_width,
            height=self.fig_subplot_height
        )
        fig.update_xaxes(title_text=settings_histogram.x_axis_title)
        fig.update_yaxes(title_text=settings_histogram.y_axis_title)
        
        return fig
        
    def build_individual_plot(self,
                          df: pd.DataFrame,
                          title: str,
                          settings_histogram : Histogram2DContourSettings
                          ) -> Figure:
        fig = make_subplots(
            rows=1,
            cols=1,
            subplot_titles=[title]
        )
        fig.add_trace(
            settings_histogram.create_histogram2dcontour(
                df = df), 
            row=1, col=1
        )
        fig.update_traces(
            contours_coloring=settings_histogram.contour_filling, 
            contours_showlines=settings_histogram.contour_show_lines
            )
        
        # set size of plot
        fig.update_layout(
            width=self.fig_suplots_width,
            height=self.fig_subplot_height
        )
        fig.update_xaxes(title_text=settings_histogram.x_axis_title)
        fig.update_yaxes(title_text=settings_histogram.y_axis_title)
        
        return fig        