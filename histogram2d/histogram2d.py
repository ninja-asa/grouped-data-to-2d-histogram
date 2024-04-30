from dataclasses import dataclass, field
import pandas as pd
import plotly.graph_objects as go


@dataclass
class Histogram2DContourSettings(object):
    min_feature_1: int = 0
    max_feature_1: int = 0
    min_feature_2: float = 0
    max_feature_2: float = 0
    feature_1_bin_size: int = 0
    feature_2_bin_size: float = 0
    hist_colorbar_min: int = 0
    hist_colorbar_max: int = 0
    colorscale: str = "greens"
    contours: dict = field(
        default_factory=lambda: {
            "showlabels": False,
            "labelfont": dict(family="Raleway", color="white"),
        }
    )
    x_axis_title: str = "Feature 1"
    y_axis_title: str = "Feature 2"
    contour_filling: str = "fill"
    contour_show_lines: bool = True
    normalized: bool = True

    def get_z_colorbar_label(self):
        if self.normalized:
            return "Percentage"
        else:
            return "Count"

    def create_histogram2dcontour(self, df: pd.DataFrame):
        if self.normalized:
            return self.create_frequency_histogram2dcontour(df)
            
        else:
            return self.create_count_histogram2dcontour(df)

    def create_count_histogram2dcontour(self, df: pd.DataFrame):
        hist_data = go.Histogram2dContour(
            x=df[self.x_axis_title],
            y=df[self.y_axis_title],
            colorscale=self.colorscale,
            contours=self.contours,
            zmin=self.hist_colorbar_min,
            zmax=self.hist_colorbar_max,
            xbins=dict(
                start=self.min_feature_1 - self.feature_1_bin_size,
                end=self.max_feature_1,
                size=self.feature_1_bin_size,
            ),
            ybins=dict(
                start=self.min_feature_2 - self.feature_2_bin_size,
                end=self.max_feature_2,
                size=self.feature_2_bin_size,
            ),
            colorbar=dict(title=self.get_z_colorbar_label()),
        )

        return hist_data

    def create_frequency_histogram2dcontour(self, df: pd.DataFrame):

        hist_data = go.Histogram2dContour(
            x=df[self.x_axis_title],
            y=df[self.y_axis_title],
            colorscale=self.colorscale,
            contours=self.contours,
            histnorm="percent",
            zmin=self.hist_colorbar_min,
            zmax=self.hist_colorbar_max,
            xbins=dict(
                start=self.min_feature_1 - self.feature_1_bin_size,
                end=self.max_feature_1,
                size=self.feature_1_bin_size,
            ),
            ybins=dict(
                start=self.min_feature_2 - self.feature_2_bin_size,
                end=self.max_feature_2,
                size=self.feature_2_bin_size,
            ),
            colorbar=dict(title=self.get_z_colorbar_label(), ticksuffix="%"),
        )

        return hist_data
