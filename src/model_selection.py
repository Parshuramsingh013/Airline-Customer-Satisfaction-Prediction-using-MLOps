from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score,recall_score,f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import lightgbm as lgb
import xgboost as xgb 

import os 
import pandas as pd 
from src.logger import get_logger
from src.custom_exception import CustomException
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from config.paths_config import *
from utils.helpers import *
import matplotlib.pyplot as plt
import time
import sys

from torch.utils.tensorboard import SummaryWriter

logger = get_logger(__name__)


class ModelSelection:

    def __init__(self, data_path):
        self.data_path = data_path
        run_id = time.strftime("%Y%m%d-%H%M%S")
        self.writer = SummaryWriter(log_dir=f"tensorboard_logs/run_{run_id}")

        self.model = {
                    'Logistic Regression': LogisticRegression(),
                    'Random Forest': RandomForestClassifier(n_estimators=50, n_jobs=-1),
                    'Gradient Boosting': GradientBoostingClassifier(n_estimators=50),
                    'AdaBoost': AdaBoostClassifier(n_estimators=50),
                    'Support Vector Classifier': SVC(),
                    'K-Nearest Neighbors': KNeighborsClassifier(),
                    'Naive Bayes': GaussianNB(),
                    'Decision Tree': DecisionTreeClassifier(),
                    'LightGBM': lgb.LGBMClassifier(),
                    'XGBoost': xgb.XGBClassifier(eval_metric='mlogloss')
                    }
        
        self.results = {}

    def load_data(self):
        try:
            logger.info(f"Loading data from")
            df = pd.read_csv(self.data_path) #100% Data
            df_sample = df.sample(frac= 0.05, random_state=42) #5% Data

            X = df_sample.drop(columns='satisfaction')
            y = df_sample['satisfaction']

            logger.info(f"Data loaded successfully")
            return X,y
        
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise CustomException(f"Error loading data", sys)
        
    def split_data(self, X, y):
        try:
            logger.info("Splitting the data into train and test sets")
            return train_test_split(X, y, test_size=0.2, random_state=42)
        
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException (f"Error splitting data", sys)
        
    def log_confusion_matrix(self, y_true, y_pred, step, model_name):
        cm = confusion_matrix(y_true, y_pred)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.matshow(cm, cmap = plt.cm.Blues, alpha= 0.7)

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(x=j, y=i, s=cm[i, j], va='center', ha='center')

        plt.xlabel('Predictions Labels')
        plt.ylabel('True/Actual Labels')
        plt.title(f'{model_name} Confusion Matrix')

        self.writer.add_figure(f"confusion_matrix/{model_name}", fig, global_step=step)
        plt.close(fig)


    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        try:
            logger.info(f"Training and evaluating models")
            for idx, (name, model) in enumerate(self.model.items()):
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                f1 = f1_score(y_test, y_pred, average='weighted', zero_division= 0)

                self.results[name] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1
                }

                logger.info(f"{name} trained model successfully"
                            f"matrics: accuracy: {accuracy}, precision: {precision}, recall: {recall}, f1_score: {f1}")
                
                self.writer.add_scalar(f"accuracy/{name}", accuracy, idx)
                self.writer.add_scalar(f"precision/{name}", precision, idx)
                self.writer.add_scalar(f"recall/{name}", recall, idx)
                self.writer.add_scalar(f"f1_score/{name}", f1, idx)

                self.writer.add_text('Model Details ' , f"Name : {name}"  f"Metrics : Accuracy : {accuracy} , Precision : {precision} , Recall : {recall} , F1 Score : {f1}" )
                
                self.log_confusion_matrix(y_test, y_pred, idx, name)

            self.writer.close()
        
        except Exception as e:
            logger.error(f"Error training and evaluating models: {e}")
            raise CustomException(f"Error training and evaluating models", sys)
        
    def run(self):
        try: 
            logger.info("Model Selection pipeline started")
            X, y = self.load_data()
            X_train, X_test, y_train, y_test = self.split_data(X, y)
            
            self.train_and_evaluate(X_train, X_test, y_train, y_test)

            logger.info("Model Selection pipeline completed")
        
        except Exception as e:
            logger.error(f"Error running model selection pipeline: {e}")
            raise CustomException(f"Error running model selection pipeline", sys)
            
if __name__ == "__main__":
    model_selection = ModelSelection(ENGINEERED_DATA_PATH)
    model_selection.run()


        




