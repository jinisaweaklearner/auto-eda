import pandas as pd
import numpy as np
import sys
import os
import argparse
import pathlib

pd.options.display.max_columns = None  # show all columns
# import modin.pandas as pd


long_desc = '''
            Welcome to the auto-eda package.
            It can help you to auto scan the dataset
            1. head of dataset
            2. tail of dataset 
            3. shape of dataset
            4. number of missing values 
            5. number of duplicated rows
            6. data type 
            7. descriptive statistics 
            8. number of unique values 
            9. unique identifies 
            10. relative frequency (precentage) of unique values or bins of numerical features
            11. unique values for each feature
            12. top absolute correlation among features 
            '''


def main():
    parser = argparse.ArgumentParser(prog='auto-eda',
                                     usage='%(prog)s file_name num_sample[option]',
                                     description=long_desc,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='If you have any advice or questions, feel free to email me xiaochengjin.random@gmail.com')
    parser.add_argument(
        dest="file", type=argparse.FileType("r"), help="file names")
    parser.add_argument(dest='num_sample', type=int,
                        help="number of samples")  # TODO: default value is all?

    args = parser.parse_args()
    args.file.close()
    print(f'Get file: {args.file.name}')
    print(args)

    df = pd.read_csv(args.file.name)

    print(f'{df.shape[0]} rows and {df.shape[1]} columns in the data frame')

    if args.num_sample > 0 and args.num_sample < 1000000:
        # if num_sample > num of rows
        eda(df, min(args.num_sample, df.shape[0]))
    else:
        raise ValueError(
            "the number of samples should be from 0 to 1000000 \n"
            "e.g. auto-eda file_name.csv 1000 \n"
        )


def eda(df, num_sample):
    '''
    the function below is a general EDA of a dataset
    to know about details about the dataset and visualize some information, we can dive deep in jupyter lab
    =================
    param
    @df: DataFrame
    '''

    df = df.sample(n=num_sample, random_state=42)

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
    print(round(df.describe(), 2))
    # categorical features
    print(round(df.describe(include=[np.object]), 2))

    # # check number of unique values for each feature
    # # it wll be very slow
    print('\n======= number of unique values =======')
    n_unique = df.nunique().tolist()
    print(df.nunique())

    # find the unique identifier
    print('\n======= find the unique identifier =======')
    for i in range(df.shape[1]):
        if n_unique[i] == len(df):
            print("{} is the unique identifier".format(df.columns[i]))

    df.dropna(axis=1, inplace=True, how='all')

    # print relative frequency (precentage) of unique values or bins of numerical features
    print('\n======= relative frequency (precentage) of unique values or bins of numerical features =======')
    for col in df.columns:

        if df[col].dtypes.name == 'object' or df[col].dtypes.name == 'category':
            print(f"{col} -- categorical feature; top 20 categories")
            print(round(df[col].value_counts(normalize=True)*100, 2)[:20])
        else:
            print(f"{col} -- numerical feature; 5 bins")
            print(round(df[col].value_counts(bins=5)))
        print('-----------------------------')

    # print unique values
    print('\n======= unique values for each feature =======')
    for col in df.columns:
        if df[col].dtypes.name == 'object' or df[col].dtypes.name == 'category':
            if df[col].nunique() < 100:
                print('column name:', col)
                print(df[col].unique())
                print('-----------------------------')
            else:
                print(f'over 100 unique values in {col}...')

    # correlation
    print('\n======= absolute correlation among features =======')
    corr_matrix = df.corr().abs()

    # the matrix is symmetric so we need to extract upper triangle matrix without diagonal (k = 1)
    sol = (corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
           .stack()
           .sort_values(ascending=False))
    # first element of sol series is the pair with the bigest correlatio
    df_corr = sol.reset_index()
    df_corr.columns = ['feat_1', 'feat_2', 'corr']
    print('Top correlated features')
    print(df_corr)

    # TODO: outlier detection
    # https://github.com/jinisaweaklearner/auto-eda/blob/master/requirements.txt

    # TODO: more vis
    # TODO: auto highlight sth
    # TODO: auto insights?

if __name__ == '__main__':
    main()
