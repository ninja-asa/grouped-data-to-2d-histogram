import pandas as pd

from histogram2d import Histogram2DContourSettings
from visualize import VisualizeSettings, Figure

class Orchestrator():
    def __init__(self, 
                 histogram2d_settings: Histogram2DContourSettings,
                 multiplot_settings: VisualizeSettings,
                 debug: bool = False,
                 ) -> None:
        self.histogram2d_settings = histogram2d_settings
        self.multiplot_settings = multiplot_settings
        self.debug = debug
        return
    
    def get_sub_df(self, df: pd.DataFrame, column_names, new_column_names):
        """
        Get a partial df containing the specified columns. Rename those column. The NaN rows will be dropped as well
        """
        sub_df: pd.DataFrame = df[column_names]
        sub_df = sub_df.drop([0])
        sub_df.rename(columns={
            column_names[0]: new_column_names[0],
            column_names[1]: new_column_names[1] 
        }, inplace=True
        )
        # set name of dataframe to be "test"
        sub_df = sub_df.dropna()
        return sub_df

    def read_data_from_excel(self, excel_filepath: str) -> list[pd.DataFrame]:
        df = pd.read_excel(excel_filepath)
        if self.debug:
            print(">>>>>RAW DATA>>>>>")
            print(df.head(6))

        new_columns_names = [
            self.histogram2d_settings.x_axis_title, 
            self.histogram2d_settings.y_axis_title
            ]
        
        df_flat = self.get_sub_df(df,['Flat', 'Unnamed: 1'], new_column_names=new_columns_names)
        df_1um = self.get_sub_df(df,['1 um', 'Unnamed: 3'], new_column_names=new_columns_names)
        df_2um = self.get_sub_df(df,['2 um', 'Unnamed: 5'], new_column_names=new_columns_names)
        df_3um = self.get_sub_df(df,['3 um', 'Unnamed: 7'], new_column_names=new_columns_names)
        df_4um = self.get_sub_df(df,['4 um', 'Unnamed: 9'], new_column_names=new_columns_names)
        df_5um = self.get_sub_df(df,['5 um', 'Unnamed: 11'], new_column_names=new_columns_names)
        
        if self.debug:
            print(">>>>>>FLAT>>>>>>")
            print(df_flat.describe())
            print(">>>>>>1 um>>>>>>")
            print(df_1um.describe())
            print(">>>>>>2 um>>>>>>")
            print(df_2um.describe())
            print(">>>>>>3 um>>>>>>")
            print(df_3um.describe())
            print(">>>>>>4 um>>>>>>")
            print(df_4um.describe())
            print(">>>>>>5 um>>>>>>")
            print(df_5um.describe())
        
        dfs = [df_flat, df_1um, df_2um, df_3um, df_4um, df_5um]
        
        return dfs        

    def get_max_min_column_value(self, dfs : list[pd.DataFrame], column_value: str):
        """
        Get the max and min value of a column across all dataframes in selected column
        """
        max_value = 0
        min_value = 0
        for df in dfs:
            max_value = max(max_value, df[column_value].max())
            min_value = min(min_value, df[column_value].min())
        return max_value, min_value

    def update_settings_with_min_max_area(self, max_area: int, min_area: int):
        """
        Update the settings with the min and max area
        """
        self.histogram2d_settings.max_area = max_area
        self.histogram2d_settings.min_area = min_area

    def update_settings_with_min_max_intensity(self, max_intensity, min_intensity):
        """
        Update the settings with the min and max intensity
        """
        self.histogram2d_settings.max_intensity = max_intensity
        self.histogram2d_settings.min_intensity = min_intensity

    
    
    def run(self, 
            excel_filepath: str,
            titles: list[str]) -> None:
        
        dfs = self.read_data_from_excel(excel_filepath=excel_filepath)
        max_area, min_area = self.get_max_min_column_value(dfs, self.histogram2d_settings.x_axis_title)
        max_intensity, min_intensity = self.get_max_min_column_value(dfs, self.histogram2d_settings.y_axis_title)
        if self.debug:
            print("Max area: ", max_area)
            print("Min area: ", min_area)
            print("Max intensity: ", max_intensity)
            print("Min intensity: ", min_intensity)

        self.update_settings_with_min_max_area(max_area, min_area)
        self.update_settings_with_min_max_intensity(max_intensity, min_intensity)
        
        fig: Figure = self.multiplot_settings.build_multiplots_figure(
            dataframes=dfs,
            titles=titles,
            settings_histogram=self.histogram2d_settings
        )
        fig.write_image("combined.pdf")

        for df, title in zip(dfs, titles):
            fig = self.multiplot_settings.build_individual_plot(
                df=df,
                title=title,
                settings_histogram=self.histogram2d_settings
            )
            fig.write_image(f"{title}.pdf")

