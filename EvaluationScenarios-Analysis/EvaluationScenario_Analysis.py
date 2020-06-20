import glob

import matplotlib.pyplot as plt
import pandas as pd

## Settings for Panda dataframe displays
pd.options.display.width = 1200
pd.options.display.max_colwidth = 100
pd.options.display.max_columns = 100

all_IBMBC_files = glob.glob("*Timestamps_IBMBC*.csv")
all_Ethereum_files = glob.glob("*Timestamps_Ether*.csv")

# print("All LCaaS-IBM Blockchain files are: ", all_IBMBC_files)
# print("All LCaaS-Ethereum files are: ", all_Ethereum_files)

## declaring columns for all the panda dataframes
data_columns_21 = ["BC_data_1", "BC_data_2", "BC_data_3", "BC_data_4", "BC_data_5", "BC_data_6", "BC_data_7",
                   "BC_data_8",
                   "BC_data_9", "BC_data_10", "BC_data_11", "BC_data_12", "BC_data_13", "BC_data_14", "BC_data_15",
                   "BC_data_16", "BC_data_17", "BC_data_18", "Start_time", "End_time", "Submission_Duration"]

data_columns_8 = ["BC_data_1", "BC_data_2", "BC_data_3", "BC_data_4", "BC_data_5", "BC_data_6", "BC_data_7",
                  "Duration_timestamp"]


def extract_scenarios(filename: str) -> str:
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
    ## As the TPS for 0.1 is represented in the files as 01, we need to convert it to 0.1
    if (filename_without_extension_seperated[3] == "01"):
        TPS = 0.1
    else:
        TPS = filename_without_extension_seperated[3]  # transaction per second
    NoDBinCB = filename_without_extension_seperated[4]  # Number of data blocks in a circled blockchain

    return TNoDB, TPS, NoDBinCB


def timestamp_to_milliseconds(timestamp):
    hours, minutes, seconds, milliseconds = [float(x) for x in timestamp.replace('.', ':').split(':')]
    # return milliseconds + 1000 * (seconds + 60 * (minutes + 60 * hours))
    return (seconds * 1000) + (milliseconds / 1000)


def parse_log_files(list_of_files: list, number_of_columns: int, graph_title: str):
    """
    :param list_of_files: This is a list containing all the .csv files that we need to parse and extract data from
    This function loads the list of csv files

    :return: pandas dataframes
    """
    aggregated_df = pd.DataFrame()
    for filename in list_of_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        if (number_of_columns == 21):
            df.columns = data_columns_21
        elif (number_of_columns == 8):
            # print("sample conversion", timestamp_to_milliseconds('0:00:10.30011'))
            df.columns = data_columns_8
            df['Submission_Duration'] = ''
            ## Constrcuting the new duration by converting timestamp to miliseconds (ms)
            for i, dur in enumerate(df['Duration_timestamp']):
                df['Submission_Duration'] = df.at[i, 'Submission_Duration'] = timestamp_to_milliseconds(dur)

        ## Extracting details from each file
        extracted_scenario_details = extract_scenarios(filename)
        df['Filename'] = filename
        df['TNoDB'] = int(extracted_scenario_details[0])
        df['TPS'] = round(float(extracted_scenario_details[1]), 1)
        df['NoDBinCB'] = int(extracted_scenario_details[2])

        ## Aggregating all dfs into one
        aggregated_df = aggregated_df.append(df)

    # print("### aggregated_df is: \n", aggregated_df)
    # print("### aggregated_df data types are: \n", aggregated_df.info())

    ## Selecting a subset of columns that are needed
    aggregated_df = aggregated_df.loc[:, ["Submission_Duration", "Filename", "TNoDB", "TPS", "NoDBinCB"]]
    # print("### aggregated_df after clean up \n", aggregated_df)

    ## Grouping the dfs based on filename (as it yields to unique scenarios)
    aggregated_grouped_df = aggregated_df.groupby(['Filename']).mean()
    # print("### aggregated_grouped_df is: \n", aggregated_grouped_df)
    # print("### aggregated_grouped_df data types are: \n", aggregated_grouped_df.info())

    #
    ## Empty lists for columns of the grouped data frame
    tps_01, tps_1, tps_10, tps_100 = ([] for i in range(4))

    ## Extracting unique duration for each scneario and add it to the data frame
    for index, row in aggregated_grouped_df.iterrows():
        if (row['TPS'] < 1):
            # print(row['TNoDB'], row['TPS'], row['NoDBinCB'], row['Duration'])
            tps_01.append(row['Submission_Duration'])
        elif (row['TPS'] == 1):
            # print(row['TNoDB'], row['TPS'], row['NoDBinCB'], row['Duration'])
            tps_1.append(row['Submission_Duration'])
        elif (row['TPS'] == 10):
            # print(row['TNoDB'], row['TPS'], row['NoDBinCB'], row['Duration'])
            tps_10.append(row['Submission_Duration'])
        elif (row['TPS'] == 100):
            # print(row['TNoDB'], row['TPS'], row['NoDBinCB'], row['Duration'])
            tps_100.append(row['Submission_Duration'])

    aggregated_grouped_graphable_df = pd.DataFrame({'0.1 TPS': tps_01, '1 TPS': tps_1,
                                                    '10 TPS': tps_10, '100 TPS': tps_100})

    aggregated_grouped_graphable_df_t = aggregated_grouped_graphable_df.T  # transpose the df

    aggregated_grouped_graphable_df_t.columns = ["TNoDB=200, NoDBinCB=1", "TNoDB=200, NoDBinCB=10",
                                                 "TNoDB=1000, NoDBinCB=100"]

    ## Plotting efforts
    ax = aggregated_grouped_graphable_df_t.plot(kind='bar', grid='True', title=graph_title,
                                                legend='False',
                                                figsize=[15, 8])
    ax.set_xlabel("Transaction per second (TPS)")
    ax.set_ylabel("Submission Duration (ms)")
    plt.xticks(rotation=0)
    plt.show()

    return aggregated_grouped_graphable_df_t


## calling the main function
IBM_BC_aggregated_grouped_graphable_df_t = parse_log_files(all_IBMBC_files, 21, "IBM Blockchain Submissions")
Ethereum_BC_aggregated_grouped_graphable_df_t = parse_log_files(all_Ethereum_files, 8,
                                                                "Ethereum Blockchain Submissions")
