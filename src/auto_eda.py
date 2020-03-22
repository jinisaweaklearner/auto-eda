import pandas as pd
import numpy as np
import sys
import os
import argparse
import pathlib
pd.options.display.max_columns = None  # show all columns
# import modin.pandas as pd


def main():
    parser = argparse.ArgumentParser(prog='auto-eda',
                                     usage='%(prog)s [options] path',
                                     description='Welcome to the auto-eda package.',
                                     epilog='If you have any advice or questions, feel free to email me xiaochengjin.random@gmail.com')
    parser.add_argument(
        dest="file", type=argparse.FileType("r"), help="file names")
    parser.add_argument(dest='num_sample', type=int, help="number of samples")

    args = parser.parse_args()
    args.file.close()
    print(f'Get file: {args.file.name}')

    df = pd.read_csv(args.file.name)

    print(f'{df.shape[0]} rows and {df.shape[1]} columns in the data frame')

    if args.num_sample > 0 and args.num_sample < 1000000:
        eda(df, args.num_sample)
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
    main()
