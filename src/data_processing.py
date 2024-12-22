import pandas as pd 
from config.paths_config import *
from src.logger import get_logger
from src.custom_exception import CustomException
import sys 

logger = get_logger(__name__)

class DataProcessor:
    
    def __init__(self):
        self.train_path = TRAIN_DATA_PATH
        self.processed_data_path = PROCESSED_DATA_PATH

    def load_data(self):
        try:
            logger.info(f"Data Processing started")
            df = pd.read_csv(self.train_path)
            logger.info(f"Data read successfully : Data Shape : {df.shape}")
            return df 
        
        except Exception as e :
            logger.error("Problem While Loading Data")
            raise CustomException("error while loading data:", sys)
        
    def drop_unnecessory_columns(self, df, columns):
        try:
            logger.info(f"Drop unnecessory columns started : {columns}")
            df = df.drop(columns= columns, axis=1)
            logger.info(f"Drop unnecessory columns completed : Shape : {df.shape}")
            return df 
        
        except Exception as e :
            logger.error("problem while droppinf columns")
            raise CustomException ("Error while dropping columns", sys)
        
    def handle_outliers(self, df, columns):
        try:
            logger.info(f"Handling Outliers started : {columns}")

            for column in columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df[column] = df[column].clip(lower = lower_bound, upper = upper_bound)
            
            logger.info(f"Handling Outliers completed : Shape : {df.shape}")
            return df 
        
        except Exception as e:
            logger.error("problem while handling outliers")
            raise CustomException ("Error while handling Outliers", sys)
        
    def handle_null_values(self, df, columns):
        try:
            logger.info(f"Handling the null values has been started : {columns}")
            df[columns] = df[columns].fillna(df[columns].median())
            logger.info(f"handling the null values been successfully completed : Shape : {df.shape}")
            return df 
        
        except Exception as e :
            logger.errro("problem While Handling the null Values")
            raise CustomException ("Error while handling the null values", sys)
        
    def save_data(self, df):
        try:
            logger.info (f"saving the data been started")
            os.makedirs(PROCESSED_DIR, exist_ok=True)
            df.to_csv(self.processed_data_path, index=False)
            logger.info(f"data has been saved Succesfully")

        except Exception as e:
            logger.error("problem while saving the data")
            raise CustomException("Error while saving the data", sys)
        
    def run(self):
        try:
            logger.info("Data Processing pipeline has been satrted")

            df = self.load_data()
            df = self.drop_unnecessory_columns(df, ["MyUnknownColumn","id"])
            columns_to_handle = ['Flight Distance','Departure Delay in Minutes','Arrival Delay in Minutes', 'Checkin service']
            df = self.handle_outliers(df, columns_to_handle)

            df = self.handle_null_values(df, 'Arrival Delay in Minutes')

            self.save_data(df)

            logger.info("Data Processing Pipeline has been completed")

        except CustomException as ce:
            logger.error(f"Problem while running the data processing pipeline : {str(ce)}")


if __name__ == "__main__":
    processor = DataProcessor()
    processor.run()
            


