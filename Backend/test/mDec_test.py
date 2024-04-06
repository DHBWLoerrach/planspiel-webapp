import pandas as pd

def read_decision_data(excel_file_path):
    # Load the Excel file
    df = pd.read_excel(excel_file_path, sheet_name='Entscheidungen')

    # Extracting data for mDec_SOLID
    # Replace 'Solid_Column_X' with the actual column names for SOLID data in your Excel sheet
    solid_columns = ['Solid_Column_1', 'Solid_Column_2', 'Solid_Column_3']
    mDec_SOLID = df[solid_columns].values

    # Extracting data for mDec_IDEAL
    # Replace 'Ideal_Column_X' with the actual column names for IDEAL data in your Excel sheet
    ideal_columns = ['Ideal_Column_1', 'Ideal_Column_2', 'Ideal_Column_3']
    mDec_IDEAL = df[ideal_columns].values

    return mDec_SOLID, mDec_IDEAL

# Path to your Excel file containing decisions
excel_file_path = 'OLD/GMS_Pro_2.1/Decisions/Entscheidungen-P07-U02.xlsx'

# Read and extract decision data
mDec_SOLID, mDec_IDEAL = read_decision_data(excel_file_path)

# Print the extracted data
print("mDec_SOLID:")
print(mDec_SOLID)
print("\nmDec_IDEAL:")
print(mDec_IDEAL)