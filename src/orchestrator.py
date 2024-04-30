import logging
import os

import pandas as pd
from datetime import datetime

from src.histogram2d import Histogram2DContourSettings
from src.visualize import VisualizeSettings, Figure
logger = logging.getLogger(__name__)
logging.basicConfig(
                    level=logging.INFO,
                    format='%(filename)s: '    
                            '%(levelname)s: '
                            '%(funcName)s(): '
                            '%(lineno)d:\t'
                            '%(message)s')

class Orchestrator:
    MAX_FEATURE_COUNT = 2
    def __init__(
        self,
        histogram2d_settings: Histogram2DContourSettings = Histogram2DContourSettings(),
        multiplot_settings: VisualizeSettings = VisualizeSettings(),
        debug: bool = False,
    ) -> None:
        self.histogram2d_settings = histogram2d_settings
        self.multiplot_settings = multiplot_settings
        self.debug = debug
        # Setup a logger which logs the current time, together with type of log, and set it to debug level
        if self.debug:
            # set the logging level to debug
            logger.setLevel(logging.DEBUG)
        else:
            # set the logging level to info
            logger.setLevel(logging.INFO)
        self.output_folder = self.prepare_outputs_folder()
        return

    def prepare_outputs_folder(self):
        """
        Prepare the outputs folder
        """
        outputs_folder = "outputs"
        if not os.path.exists(outputs_folder):
            os.makedirs(outputs_folder)
        # get datetime now and create folder with that name, without milliseconds
        outputs_folder = os.path.join(outputs_folder, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        os.makedirs(outputs_folder)           
        return outputs_folder
    
    @classmethod
    def get_groups_df(
        cls, df: pd.DataFrame
    ):
        """
        Get the groups of the dataframe. The groups are identified by the merged cells in the excel file

        Args:
            df (pd.DataFrame): dataframe, where the groups are identified by the merged cells. Whenever 
                there is a merged cell, pandas will set the first cell with the name of the group and the rest of the cells
                will be named as "unnamed: x" where x is the index of the column

        Returns:
            list[pd.Dataframe]: list of dataframes, one per group
            list[str]: list of group names
        
        Usage:
            >>> df = pd.read_excel("path_to_excel_file")
            >>> df.head(3)
            output:
            |  A  | Unnamed: 1 | Unnamed: 2 |  B  | Unnamed: 3 |
            | --- | ---------- | ---------- | --- | ---------- |
            |  F1 |        F2  |        F3  |  F1 |        F2  |
            |  1  |        2.1 |        3.1 |  3  |        2.1 |
            |  2  |        2.2 |        3.2 |  4  |        2.2 |
            >>> dfs, groups = Orchestrator.get_groups_df(df)
            >>> len(dfs)
            2
            >>> groups
            ['A', 'B']
            >>> dfs[0].head(1)
            output:
            |  F1 |  F2 |  F3 |
            | --- | --- | --- |
            |  1  | 2.1 | 3.1 |
        """

        # get group names and index of those columns
        group_column_names = [
            [column_name, idx]
            for idx, column_name in enumerate(df.columns)
            if cls.is_group_column_name(column_name)
        ]
        dfs_of_groups = []
        if len(group_column_names) == 0:
            return [df], ""
        for idx_group, group in enumerate(group_column_names):
            first_colum_of_group = group[1]
            if idx_group == len(group_column_names) - 1:
                last_column_of_group = len(df.columns)
            else:
                last_column_of_group = group_column_names[idx_group + 1][1]
            # get the columns of the group
            columns_of_group = df.columns[first_colum_of_group:last_column_of_group]
            # get the sub dataframe
            sub_df = df[columns_of_group]
            # cleanup
            sub_df = cls.cleanup_group_df(sub_df)
            # rename the columns
            dfs_of_groups.append(sub_df)
        group_names = [group[0] for group in group_column_names]
        logging.debug(f"Grouped identified: {group_names}")
        return dfs_of_groups, group_names

    @staticmethod
    def cleanup_group_df(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleanup the group dataframe by removing the first row and renaming the columns
        """
        # replace columns with the first row
        df.columns = df.iloc[0]
        # drop the first row

        df = df.drop([0])
        return df

    @staticmethod
    def is_group_column_name(column_name: str) -> bool:
        """
        Does string contain unnamed substring

        Args:
            column_name (str): column name

        Returns:
            bool: whether column name contains unnamed substring - which indicates a merged excell cells
        """
        return not "unnamed" in column_name.lower()


    def read_data_from_excel(self, excel_filepath: str):
        """
        Read data from excel file and return a list of dataframes
        
        Args:
            excel_filepath (str): path to excel file
            
        Returns:
            list[pd.DataFrame]: list of dataframes
            list[str]: list of group names
        """
        # check if file exists
        if not os.path.exists(excel_filepath):
            logging.error(f"File {excel_filepath} does not exist")
            raise FileNotFoundError(f"File {excel_filepath} does not exist")
        try:
            df = pd.read_excel(excel_filepath)
        except Exception as e:
            logging.error(f"Error reading excel file: {e}")
            raise e
        logging.debug(">>>>>RAW DATA>>>>>")
        logging.debug(df.head(6))

        dfs, groups_name = self.get_groups_df(df)
        
        for df, group_name in zip(dfs, groups_name):
            logging.debug(f">>>>>>{group_name}>>>>>>")
            logging.debug(df.describe())
        return dfs, groups_name

    @staticmethod
    def get_max_min_column_value(dfs: list[pd.DataFrame], column_value: str):
        """
        Get the max and min value of a column across all dataframes in selected column
        """
        max_value = 0
        min_value = 0
        for df in dfs:
            max_value = max(max_value, df[column_value].max())
            min_value = min(min_value, df[column_value].min())
        return max_value, min_value

    def update_settings_with_min_max_feature_1(self, max_feature_1: int, min_feature_1: int):
        """
        Update the settings with the min and max area
        """
        self.histogram2d_settings.max_feature_1 = max_feature_1
        self.histogram2d_settings.min_feature_1 = min_feature_1

    def update_xy_titles(self, x_axis_title: str, y_axis_title: str) -> None:
        """
        Update the settings with the x and y axis titles
        """
        self.histogram2d_settings.x_axis_title = x_axis_title
        self.histogram2d_settings.y_axis_title = y_axis_title
        
    def update_settings_with_min_max_feature_2(self, max_feature_2, min_feature_2):
        """
        Update the settings with the min and max intensity
        """
        self.histogram2d_settings.max_feature_2 = max_feature_2
        self.histogram2d_settings.min_feature_2 = min_feature_2

    def run(self, excel_filepath: str, features: list[str] = []) -> None:
        """
        Run the orchestrator. Read the data from the excel file, get the groups, get the features, get the features values range, update the settings, create the plots and save them.add()

        Args:
            excel_filepath (str): path to excel file
            features (list[str], optional): features to be displayed. Defaults to [].

        Raises:
            ValueError: If the first dataframe does not have at least two features
            ValueError: If the features do not exist in all dataframes
            ValueError: If the excel file does not have the expected format
        """
        dfs , groups = self.read_data_from_excel(excel_filepath=excel_filepath)
        if len(groups) == 0:
            logging.error("Did not obtain expected format of excel")
            raise ValueError("Did not obtain expected format of excel")
        logging.info(f"Groups identified: {groups}")

        features = self.get_features(features, dfs)
        logging.info(f"Features to be used: {features}")

        features_values_range = self.get_features_ranges(features, dfs)
        
        self.update_histogram_settings_based_on_features(features, features_values_range)
        logging.info(f"Settings updated: {self.histogram2d_settings}")
        fig: Figure = self.multiplot_settings.build_multiplots_figure(
            dataframes=dfs, titles=groups, settings_histogram=self.histogram2d_settings
        )
        self.write_image_to_formats(fig, "combined")
        logging.info("Combined plot saved")
        for df, title in zip(dfs, groups):
            fig = self.multiplot_settings.build_individual_plot(
                df=df, title=title, settings_histogram=self.histogram2d_settings
            )
            self.write_image_to_formats(fig, title)
            logging.info(f"Individual plot for {title} saved")
        logging.info("All plots saved")
        return None

    def write_image_to_formats(self, fig, title: str, formats: list[str]=["pdf", "svg", "png"] ) -> None:
        """
        Write the image to the specified formats.

        Args:
            fig (plotly.graph_objects.Figure): figure to be saved
            title (str): title of the file where the figure will be saved. If it contains the extension, it will be ignored
            formats (list, optional): target extensions of file. Defaults to ["pdf", "svg", "png"]

        Returns:
            : _description_
        """
        filename = os.path.join(self.output_folder, title)
        if "pdf" in formats:
            fig.write_image(f"{filename}.pdf")
        if "svg" in formats:
            fig.write_image(f"{filename}.svg")
        if "png" in formats:
            fig.write_image(f"{filename}.png")
        return None

    def update_histogram_settings_based_on_features(self, features, features_values_range) -> None:
        """
        Update the settings based on the features and their values range. Changes the attributes of the histogram2d_settings of this object

        Args:
            features (list[str]): list of features
            features_values_range (dict): dictionary with the feature as key and the range of values as value. For example:
                {
                    "Area": (100, 200),
                    "Intensity": (100, 200),
                }
        """
        self.update_xy_titles(features[0], features[1])
        self.update_settings_with_min_max_feature_1(
            features_values_range[features[0]][0], features_values_range[features[0]][1]
        )
        self.update_settings_with_min_max_feature_2(
            features_values_range[features[1]][0], features_values_range[features[1]][1]
        )
        return None

    @classmethod
    def get_features_ranges(cls, features: list[str], dfs: list[pd.DataFrame]):# -> dict[Any, Any]:
        """
        Get the range of values for each feature

        Args:
            features (list[str]): list of features. Should exist in each of the dataframes provided
            dfs (list[pd.Dataframe]): list of dataframes

        Returns:
            dict: dictionary with the feature as key and the range of values as value. For example:
                {
                    "Area": (100, 200),
                    "Intensity": (100, 200),
                }
        """
        features_values_range = {}
        for feature in features[:cls.MAX_FEATURE_COUNT]:
            max_value, min_value = cls.get_max_min_column_value(dfs, feature)
            features_values_range[feature] = (max_value, min_value)
            logging.debug(f"{feature} values range from {min_value} to {max_value}")
        return features_values_range

    def get_features(self, features, dfs):
        """
        Get the features to be used in the analysis. If the features are not provided, the first two features of the first dataframe will be used.

        Args:
            features (list[str]): column names in the dataframes. Can be provided as a empty list
            dfs (list[pd.Dataframe]): list of dataframes

        Raises:
            ValueError: If the first dataframe does not have at least two features
            ValueError: If the features do not exist in all dataframes

        Returns:
            list[str]: list of features
        """
        if len(features) == 0:
            try:
                # ensure it is a list of strings
                features = [str(column) for column in dfs[0].columns.values[:self.MAX_FEATURE_COUNT].tolist()]
            except:
                error_message = "First Group Does not have at least two features"
                logging.error(error_message)
                raise ValueError(error_message)
        # check if features exist in all dataframes
        for df in dfs:
            for feature in features:
                if feature not in df.columns:
                    error_message = f"Feature {feature} does not exist in all dataframes. \n Dataframe has columns {df.columns}"
                    logging.error(error_message)
                    raise ValueError(error_message)
        return features

    