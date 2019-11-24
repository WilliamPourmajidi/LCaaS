import pandas as pd
import numpy as np
import os

# Import from CSV to df
# Settings for Panda dataframe displays
pd.options.display.width = 1200
pd.options.display.max_colwidth = 100
pd.options.display.max_columns = 100

def cwd():
    return os.path.dirname(os.path.realpath(__import__("__main__").__file__))


data_columns = ["BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data",
                "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data", "BC_data",
                "Start_time", "End_time", "Duration"]

# 0.1 TPS
df_IBMBC_200_01_1 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\01TPS\\Timestamps_IBMBC_200_01_1.csv')
df_IBMBC_200_01_1.columns = data_columns
df_IBMBC_200_01_1['TNODB'] = 200
df_IBMBC_200_01_1['TPS'] = 0.1
df_IBMBC_200_01_1['TNODB_PCB'] = 1

df_IBMBC_200_01_10 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\01TPS\\Timestamps_IBMBC_200_01_10.csv')
df_IBMBC_200_01_10.columns = data_columns
df_IBMBC_200_01_10['TNODB'] = 200
df_IBMBC_200_01_10['TPS'] = 0.1
df_IBMBC_200_01_10['TNODB_PCB'] = 10

df_IBMBC_1000_01_100 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\01TPS\\Timestamps_IBMBC_1000_01_100.csv')
df_IBMBC_1000_01_100.columns = data_columns
df_IBMBC_1000_01_100['TNODB'] = 1000
df_IBMBC_1000_01_100['TPS'] = 0.1
df_IBMBC_1000_01_100['TNODB_PCB'] = 100

# 1 TPS
df_IBMBC_200_1_1 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\1TPS\\Timestamps_IBMBC_200_1_1.csv')
df_IBMBC_200_1_1.columns = data_columns
df_IBMBC_200_1_1['TNODB'] = 200
df_IBMBC_200_1_1['TPS'] = 1
df_IBMBC_200_1_1['TNODB_PCB'] = 1

df_IBMBC_200_1_10 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\1TPS\\Timestamps_IBMBC_200_1_10.csv')
df_IBMBC_200_1_10.columns = data_columns
df_IBMBC_200_1_10['TNODB'] = 200
df_IBMBC_200_1_10['TPS'] = 1
df_IBMBC_200_1_10['TNODB_PCB'] = 10

df_IBMBC_1000_1_100 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\1TPS\\Timestamps_IBMBC_1000_1_100.csv')
df_IBMBC_1000_1_100.columns = data_columns
df_IBMBC_1000_1_100['TNODB'] = 1000
df_IBMBC_1000_1_100['TPS'] = 1
df_IBMBC_1000_1_100['TNODB_PCB'] = 100

# 10 TPS
df_IBMBC_200_10_1 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\10TPS\\Timestamps_IBMBC_200_10_1.csv')
df_IBMBC_200_10_1.columns = data_columns
df_IBMBC_200_10_1['TNODB'] = 200
df_IBMBC_200_10_1['TPS'] = 10
df_IBMBC_200_10_1['TNODB_PCB'] = 1

df_IBMBC_200_10_10 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\10TPS\\Timestamps_IBMBC_200_10_10.csv')
df_IBMBC_200_10_10.columns = data_columns
df_IBMBC_200_10_10['TNODB'] = 200
df_IBMBC_200_10_10['TPS'] = 10
df_IBMBC_200_10_10['TNODB_PCB'] = 10

df_IBMBC_1000_10_100 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\10TPS\\Timestamps_IBMBC_1000_10_100.csv')
df_IBMBC_1000_10_100.columns = data_columns
df_IBMBC_1000_10_100['TNODB'] = 1000
df_IBMBC_1000_10_100['TPS'] = 10
df_IBMBC_1000_10_100['TNODB_PCB'] = 100

# 100 TPS
df_IBMBC_200_100_1 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\100TPS\\Timestamps_IBMBC_200_100_1.csv')
df_IBMBC_200_100_1.columns = data_columns
df_IBMBC_200_100_1['TNODB'] = 200
df_IBMBC_200_100_1['TPS'] = 100
df_IBMBC_200_100_1['TNODB_PCB'] = 1

df_IBMBC_200_100_10 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\100TPS\\Timestamps_IBMBC_200_100_10.csv')
df_IBMBC_200_100_10.columns = data_columns
df_IBMBC_200_100_10['TNODB'] = 200
df_IBMBC_200_100_10['TPS'] = 100
df_IBMBC_200_100_10['TNODB_PCB'] = 10

df_IBMBC_1000_100_100 = pd.read_csv(cwd() + '\\LCaaS-IBM-Blockchain\\100TPS\\Timestamps_IBMBC_1000_100_100.csv')
df_IBMBC_1000_100_100.columns = data_columns
df_IBMBC_1000_100_100['TNODB'] = 1000
df_IBMBC_1000_100_100['TPS'] = 100
df_IBMBC_1000_100_100['TNODB_PCB'] = 100

##################
# Stacklng all data frames into one
frames = [df_IBMBC_200_01_1, df_IBMBC_200_01_10, df_IBMBC_1000_01_100, df_IBMBC_200_1_1, df_IBMBC_200_1_10,
          df_IBMBC_1000_1_100, df_IBMBC_200_10_1, df_IBMBC_200_10_10,
          df_IBMBC_1000_10_100, df_IBMBC_200_100_1, df_IBMBC_200_100_10, df_IBMBC_1000_100_100]

vertical_stack = pd.concat(frames, axis=0)
print(vertical_stack.shape)
# print(vertical_stack)

# selecting the last 6 rows
vertical_stack_subset = vertical_stack.iloc[:, -6:]
print(vertical_stack_subset.shape)
# print(vertical_stack_subset)

# Export to CSV
export_csv = vertical_stack_subset.to_csv(r'c:\users\william\desktop\vertical_stack.csv', index=None,
                                          header=True)  # Don't forget to add '.csv' at the end of the path
print(cwd())
######################################
