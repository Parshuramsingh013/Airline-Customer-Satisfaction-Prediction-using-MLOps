### This is the simple method to run the entire pipeline. This is the main file which will be executed to run the entire pipeline. This file will call the other files in the src folder to run the pipeline. This file will call the DataIngestion, DataProcessor, FeatureEngineering and ModelTraining classes to run the pipeline. This file will also handle the exceptions and log the errors.


from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.feature_engineering import FeaturEngineering
from src.model_training import ModelTraining
from src.custom_exception import CustomException
from config.paths_config import *
from src.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    try:

        ## Data Ingestion
        ingestion = DataIngestion(raw_data_path=RAW_DATA_PATH, ingested_data_path=INGESTED_DATA_PATH)
        ingestion.create_ingested_data_dir()
        ingestion.split_data(train_path=TRAIN_DATA_PATH,test_path=TEST_DATA_PATH)


        ## Data Processing
        processor = DataProcessor()
        processor.run()


        ## Feature Engineering
        feature_engineer = FeaturEngineering()
        feature_engineer.run()

        ## Model Training
        modeltrainer = ModelTraining(data_path = ENGINEERED_DATA_PATH, params_path = PARAMS_PATH, model_save_path = MODEL_SAVE_PATH)
        modeltrainer.run()

    except CustomException as e:
        logger.error({str(e)})