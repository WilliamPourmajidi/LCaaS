import pandas as pd
import glob
import matplotlib.pyplot as plot
import os

## Settings for Panda dataframe displays
pd.options.display.width = 1200
pd.options.display.max_colwidth = 100
pd.options.display.max_columns = 100

# def cwd():
#     return os.path.dirname(os.path.realpath(__import__("__main__").__file__))


# print("The current working directory is: ", cwd())

# path_for_IBMBC_integration =  r"\combined"
# print(path_for_IBMBC_integration)

all_IBMBC_files = glob.glob("*IBM*.csv")
all_Ethereum_files = glob.glob("*Ether*.csv")

print("All LCaaS-IBM Blockchain files are: ", all_IBMBC_files)
print("All LCaaS-Ethereum files are: ", all_Ethereum_files)

data_columns = ["BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data",
                "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data",
                "Start_time", "End_time", "Duration"]


def extract_scenarios(filename):
    """
    :param filename:
    :return: substrings seperated by the seperator. Returning the Total number of data blocks(TNoDB), Transaction per second (TPS),
     Number of data blocks in a circled blockchain (NoDBinCB)
    """
    # Dropping the extension from the file name
    filename_without_extension = filename[:-4]

    # Getting the substrings from the file name with _ as seperator
    filename_without_extension_seperated = filename_without_extension.split('_')

    TNoDB = filename_without_extension_seperated[2]  # total number of data blocks
    TPS = filename_without_extension_seperated[3]  # transaction per second
    NoDBinCB = filename_without_extension_seperated[4]  # Number of data blocks in a circled blockchain

    return TNoDB, TPS, NoDBinCB


## Sanity Test for the extract_scenarios module
# my_string = extract_scenarios("Timestamps_Ether_200_01_1_6.csv")
# print("This is my original return", my_string)
# print("here you go:", my_string[2])

## Master dataframe
aggregated_IBMC_df = pd.DataFrame()

for filename in all_IBMBC_files:
    IBMC_df = pd.read_csv(filename, index_col=None, header=0)
    IBMC_df.columns = data_columns
    IBMC_df['Filename'] = filename
    scenario_details = extract_scenarios(filename)
    IBMC_df['TNoDB'] = int(scenario_details[0])
    IBMC_df['TPS'] = int(scenario_details[1])
    IBMC_df['NoDBinCB'] = int(scenario_details[2])
    # print(df)
    # print("next iteration")
    aggregated_IBMC_df = aggregated_IBMC_df.append(IBMC_df)

print(type(aggregated_IBMC_df))
print(aggregated_IBMC_df)

aggregated_IBMC_df.plot.bar(x="TNoDB", y="TPS", rot=70, title="Number of tourist visits - Year 2018");

plot.show(block=True);
