import os 
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.custom_exception import CustomException
from src.logger import get_logger
from config.paths_config import *

logger = get_logger(__name__)

class DataIngestion:

    def __init__(self, raw_data_path, ingested_data_path):
        self.raw_data_path = raw_data_path
        self.ingested_data_path = ingested_data_path
        logger.info("Data ingested started")

    def create_ingested_data_dir(self):
        try:
            os.makedirs(self.ingested_data_path, exist_ok=True)
            logger.info("directory for the ingestion created")

        except Exception as e:
            raise CustomException("error while creating directory", sys)
        
    def split_data(self,train_path,test_path,test_size=0.2, random_state= 42):

        try:
            data= pd.read_csv(self.raw_data_path)
            logger.info(f"Raw data has been loaded successfully with shape: {data.shape}")

            train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
            logger.info("data been splited successfully")

            train_data.to_csv(train_path, index = False)
            test_data.to_csv(test_path, index = False)
            logger.info("training and testing data saved successfully")

        except Exception as e:
            raise CustomException ("error while splitting the data", sys)
        

if __name__ == "__main__":

    try:
        ingestion = DataIngestion(raw_data_path=RAW_DATA_PATH, ingested_data_path=INGESTED_DATA_PATH)
        ingestion.create_ingested_data_dir()
        ingestion.split_data(train_path=TRAIN_DATA_PATH,test_path=TEST_DATA_PATH)

    except CustomException as ce:
        logger.info(str(ce))
        
