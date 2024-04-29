from dataclasses import dataclass, field
from typing import Literal
import pandas as pd
import plotly.graph_objects as go

@dataclass
class Histogram2DContourSettings(object):
    min_area : int = 0
    max_area : int = 0
    min_intensity : float = 0
    max_intensity : float = 0
    area_bin_size : int = 0
    intensity_bin_size: float = 0
    count_min : int = 0
    count_max : int = 0
    colorscale: str = 'greens'
    contours : dict = field(default_factory=lambda:{
        'showlabels': False,
        'labelfont': dict(
            family = 'Raleway',
            color = 'white'
        )
    })
    x_axis_title: str = 'Area'
    y_axis_title: str = 'Intensity'
    contour_filling: str = 'fill'
    contour_show_lines: bool = True
    normalized : bool = True
    
    def get_z_colorbar_label(self) -> Literal['Frequency'] | Literal['Count']:
        if self.normalized:
            return 'Frequency'
        else:
            return 'Count'

    def create_histogram2dcontour(self,
                                    df: pd.DataFrame):
        if self.normalized:
            return self.create_frequency_histogram2dcontour(df)
        else:
            return self.create_count_histogram2dcontour(df)


    def create_count_histogram2dcontour(self, 
                                  df: pd.DataFrame):
        hist_data = go.Histogram2dContour(
            x = df[self.x_axis_title],
            y = df[self.y_axis_title],
            colorscale = self.colorscale,
            contours = self.contours,
            # zmin=self.count_min,
            # zmax=self.count_max,
            xbins=dict(
                start=self.min_area - self.area_bin_size,
                end=self.max_area,
                size=self.area_bin_size
            ),
            ybins=dict(
                start=self.min_intensity - self.intensity_bin_size,
                end=self.max_intensity,
                size=self.intensity_bin_size
            )

        )
        
        return hist_data

    def create_frequency_histogram2dcontour(self, 
                                  df: pd.DataFrame):
        # create a pandas series with the same length as the dataframe, but with the same value, 100/len(df)
        # this is to create a frequency histogram
        hist_data = go.Histogram2dContour(
            x = df[self.x_axis_title],
            y = df[self.y_axis_title],
            # z = df_frequency,
            colorscale = self.colorscale,
            contours = self.contours,
            histnorm='percent',
            zmin=self.count_min,
            zmax=self.count_max,
            xbins=dict(
                start=self.min_area - self.area_bin_size,
                end=self.max_area,
                size=self.area_bin_size
            ),
            ybins=dict(
                start=self.min_intensity - self.intensity_bin_size,
                end=self.max_intensity,
                size=self.intensity_bin_size
            )

        )
        
        return hist_data