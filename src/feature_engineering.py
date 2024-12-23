import os 
import pandas as pd 
from src.logger import get_logger
from src.custom_exception import CustomException
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from config.paths_config import *
from utils.helpers import *
import sys

logger = get_logger(__name__)

class FeaturEngineering:

    def __init__(self):
        self.data_path = PROCESSED_DATA_PATH
        self.df = None
        self.label_mapping = {}

    def load_data(self):
        try:
            logger.info("Loading Data started ")
            self.df = pd.read_csv(self.data_path)
            logger.info ("data loaded successfully")
        except Exception as e:
            logger.error(f"error while loadfing the data{e}")
            raise Exception (f"error while loading data", sys)
        
    def feature_construction(self):
        try:
            logger.info(f"feature Construction started")
            self.df['Total Delay'] = self.df['Departure Delay in Minutes'] + self.df['Arrival Delay in Minutes']
            self.df['Delay Ratio'] = self.df['Total Delay'] / (self.df['Flight Distance'] + 1)
            logger.info(f"feature construction done")
        except Exception as e:
            logger.error(f"error while feature construction: {e}")
            raise CustomException (f"error while feature constrution", sys)
        
    def bin_age(self):
        try:
            logger.info(f"binning the age  been started")
            self.df['Age Group'] = pd.cut(self.df['Age'], bins=[0, 18, 30, 50, 100], labels=['Child', 'Youngster', 'Adult', 'Senior'])
            logger.info(f"binning age been done")
        except Exception as e:
            logger.error(f"error while binning age: {e}")
            raise CustomException (f"error while binning age", sys)
        

    def label_encoding(self):
        try:
            columns_to_encode = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'satisfaction', 'Age Group']
            logger.info(f"performing the label encode on {columns_to_encode}")

            self.df, self.label_mapping = label_encode(self.df, columns_to_encode)
            
            for col, mapping in self.label_mapping.items():
                logger.info(f"mapping for the {col} : {mapping}")
            logger.info(f"label encoding been done")

        except Exception as e:
            logger.error(f"error while lebel encoding: {e}")
            raise CustomException (f"error while label encoding", sys)
        

    def feature_selection(self):
        try:
            logger.info(f"feature selection started")
            X = self.df.drop(columns='satisfaction')
            y = self.df['satisfaction']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            mutual_info = mutual_info_classif(X_train, y_train, discrete_features=True)

            mutual_info_df = pd.DataFrame({
                'Feature': X.columns,
                'Mutual Information': mutual_info
                }).sort_values(by='Mutual Information', ascending=False)
            
            logger.info(f"Mutual information table is : \n {mutual_info_df}")

            top_features = mutual_info_df.head(12)['Feature'].tolist()

            self.df = self.df[top_features + ['satisfaction']]
            logger.info(f"top Features : {top_features}")
            logger.info(f"feature selection done")

        except Exception as e:
            logger.error(f"error while feature selection : {e}")
            raise CustomException (f"error while feature selection ", sys)
        
    def save_data(self):
        try:
            logger.info("saving your data........")
            os.makedirs(ENGINEERED_DATA, exist_ok=True)
            self.df.to_csv(ENGINEERED_DATA_PATH, index = False)
            logger.info(f"Data saved succesfull at : {ENGINEERED_DATA_PATH}")

        except Exception as e:
            logger.info(f"error while saving the data  {e}")
            raise CustomException (f"error while saving the data", sys)
    
    def run(self):
        try:
            logger.info("starting you feature engineering pipeline")
            self.load_data()
            self.feature_construction()
            self.bin_age()
            self.label_encoding()
            self.feature_selection()
            self.save_data()
            logger.info("Feature engineering pipeline beed ended")

        except Exception as e:
            logger.error(f"error in FE pipeline {e}")
            raise CustomException (f"error while FE pipeline")
        
        finally:
            logger.info("Feature engineering pipeline ended")
        
if __name__ == "__main__":
    
    feature_engineer = FeaturEngineering()
    feature_engineer.run()

            
    
        
    
        

        
