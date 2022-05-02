
import pandas as pd 
# My code
from one_hot_encoder import one_hot_ecoding

df = pd.read_csv('actions_taken_1-3_year_2020.csv')

print('DataFrame Shape: ', df.shape, '\n')

df = df[df['loan_type'] == 1]

y_variable = ['action_taken']

loan_characteristics = ['loan_amount',
                        'loan_to_value_ratio', 
                        'interest_rate', 
                        'loan_purpose'] 
                        #'loan_type']

applicant_finances = ['income']
                      #'debt_to_income_ratio', 
                      #'applicant_credit_score_type'] 

geography = ['state_code', 
             'county_code', 
             'census_tract', 
             'tract_population',
             'tract_minority_population_percent',
             'ffiec_msa_md_median_family_income',
             'tract_to_msa_income_percentage',
             'tract_owner_occupied_units',
             'tract_one_to_four_family_homes',
             'tract_to_msa_income_percentage']

applicant_characteristics = ['applicant_ethnicity-1', 
                            'applicant_race-1',
                            'applicant_sex']

# Filtering Dataframe columns 
in_columns = y_variable + loan_characteristics + applicant_finances + geography + applicant_characteristics                 
df = df[in_columns] 

# Binning out subcategories 
hispanic_binning = {11: 'Hispanic or Latino', 
                    1: 'Hispanic or Latino',
                    12: 'Hispanic or Latino', 
                    13: 'Hispanic or Latino', 
                    14: 'Hispanic or Latino',
                    2:  'Not Hispanic or Latino'}
race_binning = {1: 'Other', 
                21:'Asian',
                22:'Asian',
                23: 'Asian', 
                24: 'Asian', 
                25: 'Asian',
                26: 'Asian',
                27:'Asian',
               3: 'Black',
               41: 'Other',
               42: 'Other',
               43: 'Other',
               44: 'Other',
               5: 'White'}

sex_binning =  {1: 'Male', 
                2: 'Female'}

loan_purpose = {1: 'Home purchase', 
                2: 'Home improvement',
                3: 'Refinancing'}

# For our regression 
loan_outcome = {3: 0} 

df.replace({'applicant_ethnicity-1': hispanic_binning, 
            'applicant_race-1': race_binning,
            'applicant_sex': sex_binning,
            'loan_purpose': loan_purpose,
            'action_taken': loan_outcome}
            ,inplace=True)

# # Drop values
df = df[df['applicant_sex'].isin(list(set(sex_binning.values())))]
print(df['applicant_sex'].value_counts(), '\n')

df = df[df['applicant_race-1'].isin(list(set(race_binning.values())))]
print(df['applicant_race-1'].value_counts(), '\n')

df = df[df['loan_purpose'].isin(list(set(loan_purpose.values())))]
print(df['loan_purpose'].value_counts(), '\n')

df = df[df['applicant_ethnicity-1'].isin(list(set(hispanic_binning.values())))]
print(df['applicant_ethnicity-1'].value_counts(), '\n')

one_hot_columns = ['loan_purpose', 
                   'applicant_ethnicity-1', 
                   'applicant_race-1', 
                   'applicant_sex', 
                   'state_code']

new_df = one_hot_ecoding(one_hot_columns, df, drop=False)

# Convert Units
new_df['loan_amount'] = new_df['loan_amount'] / 1_000

# # Normalize raw numbers by converting into per capita 
new_df['owner_occupied_per_capita'] = new_df['tract_owner_occupied_units'] / (new_df['tract_population'] / 100)
new_df['family_units_per_capita'] = new_df['tract_one_to_four_family_homes'] / (new_df['tract_population'] / 100)
# Create interaction terms 
new_df['loan_income_ratio'] = new_df['loan_amount'] / new_df['income']
print('Final Dataframe Shape: ', new_df.shape)

# Cols we want to use in our regression 
cols = new_df.columns
state_cols = [col for col in cols if 'state_code' in col and col != 'state_code']
ethnicity_cols = [col for col in cols if 'applicant_ethnicity' in col and col != 'applicant_ethnicity-1']
race_cols = [col for col in cols if 'applicant_race-1' in col and col != 'applicant_race-1']
loan_type_cols = [col for col in cols if 'loan_purpose' in col and col != 'loan_purpose']

normal_geo_cols = ['tract_to_msa_income_percentage', 
                   'owner_occupied_per_capita', 
                   'family_units_per_capita',
                   'tract_minority_population_percent',
                   'tract_to_msa_income_percentage']

sex_cols = ['applicant_sex_Male', 'applicant_sex_Female']
more_cols = ['loan_amount','loan_to_value_ratio', 'interest_rate', 'loan_income_ratio', 'income']
regression_cols = y_variable + race_cols + ethnicity_cols + sex_cols + loan_type_cols +  normal_geo_cols + more_cols + state_cols
regression_df = new_df[regression_cols]

# First lets rename out variables to get cleaner labels 
numerical_vars = {'income': 'Applicant Income',
                 'loan_amount': 'Loan Amount',
                 'tract_minority_population_percent': '% Minority', 
                 'tract_to_msa_income_percentage': 'Tract to MSA Income Ratio', 
                 'owner_occupied_per_capita': 'Owner Occupied Per Capita',
                 'family_units_per_capita': 'Family Units Per Capita'}

dummy_vars = {'applicant_ethnicity-1_Not Hispanic or Latino': 'Not Hispanic',
                   'applicant_ethnicity-1_Hispanic or Latino': 'Hispanic',
                   'applicant_sex_Male': 'Male',
                   'applicant_sex_Female':'Female', 
                   'applicant_race-1_Asian': 'Asian',
                   'applicant_race-1_Black': 'Black',
                   'applicant_race-1_White': 'White',
                   'applicant_race-1_Other': 'Other',
                   'loan_purpose_Refinancing': 'Refinancing', 
                   'loan_purpose_Home improvement': 'Home Improvement',
                   'loan_purpose_Home purchase': 'Home Purchase'}

target_var = {'action_taken_name': 'Loan Approved'}

regression_df = regression_df.rename(columns=numerical_vars)
regression_df = regression_df.rename(columns=dummy_vars)
regression_df = regression_df.rename(columns=target_var)
regression_df['Minority'] = regression_df['Hispanic'] + regression_df['Asian'] + regression_df['Black'] + regression_df['Other']
regression_df['Minority'] = regression_df['Minority'].apply(lambda x: 1 if x >= 1 else 0)
print('Regression DataFrame: ', regression_df.shape)
for col in regression_df.columns:
    print(col)
    
rename_lookup = {'action_taken': 'Loan Approved', 
                 'loan_to_value_ratio': 'Loan-Value Ratio', 
                 'interest_rate': 'Interest Rate',
                'loan_income_ratio': 'Loan-Income Ratio'}
regression_df.rename(columns=rename_lookup, inplace=True)

regression_df.to_csv('Cleaned Data.csv')

