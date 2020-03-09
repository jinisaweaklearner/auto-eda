import pandas as pd
import numpy as np
import sys
import os
# import modin.pandas as pd


# os.environ["MODIN_ENGINE"] = "ray"  # Modin will use Ray

'''
the function below is a general EDA of a dataset
to know about details about the dataset and visualize some information, we can dive deep in jupyter lab
=================
param
df: dataframe
'''
def eda(df):

    df = df.sample(n = 10000)

    # head of dataset
    print('======= head of data =======')
    print(df.head())
    
    # tail of dataset
    print('\n======= tail of data =======')
    print(df.tail())

    # check the shape of data
    print('\n======= shape of data =======')
    print(df.shape)

    # check missing values
    print('\n======= check missing values =======')
    print(df.isnull().sum())

    # check duplicated rows
    print('\n======= check duplicated rows =======')
    print(df[df.duplicated()].shape)

    # check the data type of columns
    print('\n======= data type =======')
    print(df.dtypes)

    # generate descriptive statistics
    print('\n======= generate descriptive statistics =======')
    # numerical features
    print(round(df.describe(),2))
    # categorical features
    print(round(df.describe(include=[np.object]),2))

    # # check number of unique values for each feature
    # # it wll be very slow 
    print('\n======= number of unique values =======')
    n_unique = df.nunique().tolist()
    print(n_unique)

    # find the unique identifier
    print('\n======= find the unique identifier =======')
    for i in range(df.shape[1]):
        if n_unique[i] == len(df):
            print("{} is the unique identifier".format(df.columns[i]))

    df.dropna(axis=1,inplace=True,how='all')

    # print relative frequency (precentage) of unique values or bins of numerical features
    print('\n======= relative frequency (precentage) of unique values or bins of numerical features =======')
    for col in df.columns:
        
        if df[col].dtypes.name == 'object' or df[col].dtypes.name == 'category':
            print(f"{col} -- categorical feature; top 20 categories")
            print(round(df[col].value_counts(normalize=True)*100,2)[:20])
        else:
            print(f"{col} -- numerical feature; 5 bins")
            print(round(df[col].value_counts(bins=5)))
        print('-----------------------------')


    # print unique values
    print('\n======= unique values for each feature =======')
    for col in df.columns:
        if df[col].dtypes.name == 'object' or df[col].dtypes.name == 'category':
            if df[col].nunique() < 3000:
                print('column name:', col)
                print(df[col].unique())
                print('-----------------------------')
            else:
                print('unique values are over 3000...')
    
    # TODO: update the cor function
    # correlation and outliers
    # print('\n======= correlation between features =======')

if __name__ == '__main__':
    DATA_PATH = sys.argv[1]
    # try:
    #     df = pd.read_excel(DATA_PATH)
    # except:
    df = pd.read_csv(DATA_PATH)
    pd.options.display.max_columns = df.shape[1] # show all columns    
    eda(df)