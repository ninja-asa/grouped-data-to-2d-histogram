from plotly.subplots import make_subplots
from plotly.graph_objects import Figure
import pandas as pd
from histogram2d.builder import Histogram2DContourSettings
from dataclasses import dataclass


@dataclass
class VisualizeSettings(object):
    horizontal_spacing: float = 0.08
    vertical_spacing: float = 0.15
    fig_suplots_width: int = 1600
    fig_subplot_height_per_row: int = 400

    def build_multiplots_figure(
        self,
        dataframes: list[pd.DataFrame],
        titles: list[str],
        settings_histogram: Histogram2DContourSettings,
    ) -> Figure:
        # for len of dataframes, create a subplot 3xn necessary to display all dataframes
        numbers_cols = 3
        numbers_rows = len(dataframes) // numbers_cols
        if len(dataframes) % numbers_cols != 0:
            numbers_rows += 1
        specs = [[{"type": "histogram2dcontour"}] * numbers_cols] * numbers_rows
        column_widths = [1, 1, 1]
        row_heights = [1] * numbers_rows

        fig = make_subplots(
            rows=numbers_rows,
            cols=numbers_cols,
            subplot_titles=titles,
            horizontal_spacing=self.horizontal_spacing,
            vertical_spacing=self.vertical_spacing,
            specs=specs,
            column_widths=column_widths,
            row_heights=row_heights,
        )
        for i, df in enumerate(dataframes):
            row = i // numbers_cols + 1
            col = i % numbers_cols + 1
            fig.add_trace(
                settings_histogram.create_histogram2dcontour(df=df),
                row=row,
                col=col,
            )

        fig.update_traces(
            contours_coloring=settings_histogram.contour_filling,
            contours_showlines=settings_histogram.contour_show_lines,
        )
        # set size of plot
        fig.update_layout(
            width=self.fig_suplots_width, height=self.fig_subplot_height_per_row * numbers_rows
        )
        fig.update_xaxes(title_text=settings_histogram.x_axis_title)
        fig.update_yaxes(title_text=settings_histogram.y_axis_title)

        return fig

    def build_individual_plot(
        self,
        df: pd.DataFrame,
        title: str,
        settings_histogram: Histogram2DContourSettings,
    ) -> Figure:
        fig = make_subplots(rows=1, cols=1, subplot_titles=[title])
        fig.add_trace(settings_histogram.create_histogram2dcontour(df=df), row=1, col=1)
        fig.update_traces(
            contours_coloring=settings_histogram.contour_filling,
            contours_showlines=settings_histogram.contour_show_lines,
        )

        # set size of plot
        fig.update_layout(width=self.fig_suplots_width, height=self.fig_subplot_height_per_row)
        fig.update_xaxes(title_text=settings_histogram.x_axis_title)
        fig.update_yaxes(title_text=settings_histogram.y_axis_title)

        return fig
