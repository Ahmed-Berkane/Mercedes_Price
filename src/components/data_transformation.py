import os
import sys 
import pandas as pd 
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    
    
class DataTransformation:
    def __init__(self):
        self.DataTransformationConfig = DataTransformationConfig()
        
    def get_data_transformer_object(self):
        try:
            #num_attribs = ['Mileage', 'Rating', 'Review Count', 'Year']
            #cat_attribs = ['Adj_Name']
                
            num_attribs = ["writing score", "reading score"]
            cat_attribs = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]
                
            num_pipeline = Pipeline(
                         steps = [
                         #('new_features', AddNumFeatures(add_New_Features = False)),
                         ('imputer', SimpleImputer(strategy = "median")),
                         ('std_scaler', StandardScaler())
                            ]
                                        )
                
            cat_pipeline = Pipeline(
                          steps = [
                          #('adding_new_name', AddCatFeatures(mapping_dict, add_New_Name = False)),
                          ("imputer", SimpleImputer(strategy = "most_frequent")),
                          ('onehot', OneHotEncoder(drop ='first'))      # One-hot encode with drop first column
                            ]
                                        )
                
            logging.info('Numerical columns scaling completed')
            logging.info('Categorical columns encoding completed')
                
            preprocessor = ColumnTransformer(
                          [
                          ("num", num_pipeline, num_attribs),
                          ("cat", cat_pipeline, cat_attribs)
                           ]
                                        )
            return preprocessor
                
        except Exception as e:
            raise CustomException(e, sys)
            
            
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info('Read train and test data completed')
            
            logging.info('Obtaining preprocessing object')
            
            preprocessing_obj = self.get_data_transformer_object()
            
            #target_column_name = 'Price'
            #num_attribs = ['Mileage', 'Rating', 'Review Count', 'Year']
            #cat_attribs = ['Adj_Name']
            
            target_column_name = "math score"  
            num_attribs = ["writing score", "reading score"]
            cat_attribs = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]
            
            
            input_feature_train_df = train_df.drop(columns = [target_column_name], axis = 1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns = [target_column_name], axis = 1)
            target_feature_test_df = test_df[target_column_name]
            
            
            logging.info('Applying preprocessing object on training and testing dataframes')
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object.")
            
            save_object(

                file_path = self.DataTransformationConfig.preprocessor_obj_file_path,
                obj = preprocessing_obj

            )
            
            return (
                train_arr,
                test_arr,
                self.DataTransformationConfig.preprocessor_obj_file_path
            )
        
        except Exception as e:
                raise CustomException(e, sys)
