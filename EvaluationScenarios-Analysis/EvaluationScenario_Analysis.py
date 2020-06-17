import pandas as pd
import glob
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import os

## Settings for Panda dataframe displays
pd.options.display.width = 1200
pd.options.display.max_colwidth = 100
pd.options.display.max_columns = 100

all_IBMBC_files = glob.glob("*Timestamps_IBMBC*.csv")
all_Ethereum_files = glob.glob("*Timestamps_Ether*.csv")

# print("All LCaaS-IBM Blockchain files are: ", all_IBMBC_files)
# print("All LCaaS-Ethereum files are: ", all_Ethereum_files)

## declaring columns for all the panda dataframes
data_columns = ["BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data",
                "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data",
                "Start_time", "End_time", "Duration"]


def extract_scenarios(filename):
    """
    :param filename:
        the name of the filename that we want to extract details from

    :return: substrings seperated by the seperator. Returning the Total number of data blocks(TNoDB), Transaction per second (TPS),
     Number of data blocks in a circled blockchain (NoDBinCB)
    """
    # Dropping the extension from the file name
    filename_without_extension = filename[:-4]

    # Getting the substrings from the file name with _ as seperator
    filename_without_extension_seperated = filename_without_extension.split('_')
    # print(type(filename_without_extension_seperated))
    TNoDB = filename_without_extension_seperated[2]  # total number of data blocks
    if (filename_without_extension_seperated[3] == "01"):
        TPS = 0.1
    else:
        TPS = filename_without_extension_seperated[3]  # transaction per second
    NoDBinCB = filename_without_extension_seperated[4]  # Number of data blocks in a circled blockchain

    return TNoDB, TPS, NoDBinCB


## Aggregated dataframe from all CSVs
aggregated_IBMBC_df = pd.DataFrame()

# TODO: Convert this to a function that can be called for both IBM and Ethereum
for filename in all_IBMBC_files:
    IBMBC_df = pd.read_csv(filename, index_col=None, header=0)
    IBMBC_df.columns = data_columns
    scenario_details = extract_scenarios(filename)
    IBMBC_df['Filename'] = filename
    IBMBC_df['TNoDB'] = int(scenario_details[0])
    # IBMBC_df['TPS'] = float(scenario_details[1])
    IBMBC_df['TPS'] = round(float(scenario_details[1]), 1)
    IBMBC_df['NoDBinCB'] = int(scenario_details[2])
    # IBMBC_df['Duration_Mean'] = IBMBC_df['Duration'].mean()

    # print(IBMBC_df)
    # print("next iteration")
    aggregated_IBMBC_df = aggregated_IBMBC_df.append(IBMBC_df)

# print(aggregated_IBMBC_df.info())
# print(aggregated_IBMBC_df)

## Convert to CSV
# aggregated_IBMBC_df.to_csv('aggregated_IBMC_df.csv')

grouped_df = aggregated_IBMBC_df.groupby(['Filename']).mean()
# print("grouped_df is \n", grouped_df)
tps_01 = []
tps_1 = []
tps_10 = []
tps_100 = []
for index, row in grouped_df.iterrows():
    if (row['TPS'] < 1):
        # print(row['TNoDB'], row['TPS'], row['NoDBinCB'], row['Duration'])
        tps_01.append(row['Duration'])
    elif (row['TPS'] == 1):
        # print(row['TNoDB'], row['TPS'], row['NoDBinCB'], row['Duration'])
        tps_1.append(row['Duration'])
    elif (row['TPS'] == 10):
        # print(row['TNoDB'], row['TPS'], row['NoDBinCB'], row['Duration'])
        tps_10.append(row['Duration'])
    elif (row['TPS'] == 100):
        # print(row['TNoDB'], row['TPS'], row['NoDBinCB'], row['Duration'])
        tps_100.append(row['Duration'])
IBMBC_Graph_df = pd.DataFrame({'0.1 TPS': tps_01, '1 TPS': tps_1,
                               '10 TPS': tps_10, '100 TPS': tps_100})
# print("before pivot\n", IBMBC_Graph_df)
IBMBC_Graph_df_t = IBMBC_Graph_df.T  # transpose the df
df_t_columns = ["TNoDB=200, NoDBinCB=1", "TNoDB=200, NoDBinCB=10", "TNoDB=1000, NoDBinCB=100"]
IBMBC_Graph_df_t.columns = df_t_columns
# print("after pivot\n", IBMBC_Graph_df_t)
# IBMBC_Graph_df_t.plot(kind='bar', grid='True', title='IBM Blockchain Submission', legend='True', figsize=[15, 8])

ax = IBMBC_Graph_df_t.plot(kind='bar', grid='True', title='IBM Blockchain Submission', legend='False', figsize=[15, 8])
ax.set_xlabel("Transaction per second(TPS)")
ax.set_ylabel("Submission Duration(ms)")
plt.xticks(rotation=0)
plt.show()

