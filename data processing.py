
#%%
import pandas as pd



#%%
# Step 1 - Get solution.
# This function reformats the data in the 'act' column.
def reformat(input_file_path, output_file_path):
    # Read the Excel file as a pandas dataframe
    df = pd.read_excel(input_file_path)

    # Create a new 'session id' column.
    df['session id'] = 1

    # Create a new 'duration (sec)' column.
    df['duration (sec)'] = ''

    # Create a new 'student response type' column.
    df['student response type'] = ''

    # Create a new 'tutor response type' column.
    df['tutor response type'] = ''

    # Create a new 'level (default)' column.
    df['level (default)'] = 'programming'

    # Rename the 'did_id' column to 'problem name'
    df.rename(columns={'div_id': 'problem name'}, inplace=True)

    df['problem start time'] = ''

    df.rename(columns={'sid': 'anon student id'}, inplace=True)

    # Split the 'act' column into multiple columns
    df[['event', 'act']] = df['act'].str.split('|', n=1, expand=True)

    # Function to extract values from 'act' column
    def extract_values(row):
        if row['act']:
            parts = row['act'].split('|')
            if len(parts) == 3:
                row['source'] = parts[0]
                row['solution'] = parts[1]
                row['checked_status'] = parts[2]
        return row

    # Apply the function to extract values from 'act' column
    df = df.apply(extract_values, axis=1)

    # Split the values in 'solution' column into separate rows
    df_solution = df['solution'].str.split('-', expand=True).stack().reset_index(level=1, drop=True)
    df_solution.name = 'solution'
    df_solution = df.drop('solution', axis=1).join(df_solution).reset_index(drop=True)

    # Reorder the columns
    df_result = df_solution[['line', 'anon student id', 'session id', 'timestamp', 'duration (sec)', 'student response type', 'tutor response type', 'level (default)', 'problem name', 'problem start time', 'event', 'act', 'source', 'solution', 'checked_status', 'chapter', 'subchapter', 'study']]

    # Write the reformatted data to a new Excel file
    df_result.to_excel(output_file_path, index=False)

    print(f"Reformatted data saved to {output_file_path}")

input_file_path = '/Users/cchmagyar/Desktop/pp_data_for_learning_curve_analysis.xlsx'
output_file_path = '/Users/cchmagyar/Desktop/results.xlsx'
reformat(input_file_path, output_file_path)
#%%



#%%
# Step 2 - Add code to solution.
def getcode(input_file_path, output_file_path):
    # Read the Excel file into a DataFrame.
    df = pd.read_excel(input_file_path)

    # Create a new 'step name' column.
    df['step name'] = ''
    # Create a new 'code' column.
    df['code'] = ''
    # Create a new 'distractor block' column.
    df['distractor block'] = ''

    # Iterate over each row and populate the 'code' column based on conditions.
    for index, row in df.iterrows():
        problem_name = row['problem name']
        solution = str(row['solution'])
        study = row['study']
        
        # This code is specific to the problem and solution that starts with the first number in the solution.
        # For example, '3' in '3_1'. 
        # The first number '3' is the line number in the solution and the second number '1' is indentation (4 spaces in Python).
        if problem_name == 'exp1_pp1a' and study == 'wn20':
            if solution.startswith('0_'):
                df.at[index, 'code'] = 'def has22(nums):'
            elif solution.startswith('1_'):
                df.at[index, 'code'] = 'i = 1'
            elif solution.startswith('2_'):
                df.at[index, 'code'] = 'i = 1'
                df.at[index, 'distractor block'] = 'i = 0'
            elif solution.startswith('3_'):
                df.at[index, 'code'] = 'while i < len(nums):'
            elif solution.startswith('4_'):
                df.at[index, 'code'] = 'if nums[i] == 2 and nums[i-1] == 2:'
            elif solution.startswith('5_'):
                df.at[index, 'code'] = 'if nums[i] == 2 and nums[i-1] == 2:'
                df.at[index, 'distractor block'] = 'if nums[i] == 2 and nums[i+1] == 2:'
            elif solution.startswith('6_'):
                df.at[index, 'code'] = 'return True'
            elif solution.startswith('7_'):
                df.at[index, 'code'] = 'return True'
                df.at[index, 'distractor block'] = 'return true'
            elif solution.startswith('8_'):
                df.at[index, 'code'] = 'i += 1'
            elif solution.startswith('9_'):
                df.at[index, 'code'] = 'return False'
        
        elif problem_name == 'exp1_pp1a' and study == 'wn21':
            if solution.startswith('0_'):
                df.at[index, 'code'] = 'def has22(nums):'
            elif solution.startswith('1_'):
                df.at[index, 'code'] = 'for i in range(len(nums)-1):'
            elif solution.startswith('2_'):
                df.at[index, 'code'] = 'for i in range(len(nums)-1):'
                df.at[index, 'distractor block'] = 'for i in range(len(nums)):'
            elif solution.startswith('3_'):
                df.at[index, 'code'] = 'if nums[i] == 2 and num[i+1] == 2:'
            elif solution.startswith('4_'):
                df.at[index, 'code'] = 'if nums[i] == 2 and num[i+1] == 2:'
                df.at[index, 'distractor block'] = 'if nums[i] == 2 and num[i-1] == 2:'
            elif solution.startswith('5_'):
                df.at[index, 'code'] = 'return True'
            elif solution.startswith('6_'):
                df.at[index, 'code'] = 'return True'
                df.at[index, 'distractor block'] = 'return true'
            elif solution.startswith('7_'):
                df.at[index, 'code'] = 'return False'
        
        elif problem_name == 'exp1_pp3' and (study == 'wn20' or study == 'wn21'):
            if solution.startswith('0_'):
                df.at[index, 'code'] = 'def diffMaxMin(nums):'
            elif solution.startswith('1_'):
                df.at[index, 'code'] = 'def diffMaxMin(nums):'
                df.at[index, 'distractor block'] = 'def diffMaxMin(nums)'
            elif solution.startswith('2_3_'):
                df.at[index, 'code'] = 'large = max(nums)\n small = min(nums)'
            elif solution.startswith('2_') and not solution.startswith('2_3_'):
                df.at[index, 'code'] = 'large = max(nums)'
            elif solution.startswith('3_'):
                df.at[index, 'code'] = 'small = min(nums)'
            elif solution.startswith('4_'):
                df.at[index, 'code'] = 'return large - small'
            elif solution.startswith('5_'):
                df.at[index, 'code'] = 'return large - small'
                df.at[index, 'distractor block'] = 'return small - large'
        
        elif problem_name == 'exp1_q5_pp' and (study == 'wn20' or study == 'wn21'):
            if solution.startswith('0_'):
                df.at[index, 'code'] = 'def get_names(list_of_dict):'
            elif solution.startswith('1_') and not solution.startswith('10_'):
                df.at[index, 'code'] = 'name_list = []'
            elif solution.startswith('2_'):
                df.at[index, 'code'] = 'for p_dict in list_of_dict:'
            elif solution.startswith('3_4_'):
                df.at[index, 'code'] = 'first = p_dict.get(\'first\', \'Unknown\')\n last = p_dict.get(\'last\', \'Unknown\')'
            elif solution.startswith('5_6_'):
                df.at[index, 'code'] = 'first = p_dict.get(\'first\', \'Unknown\')\n last = p_dict.get(\'last\', \'Unknown\')'
                df.at[index, 'distractor block'] = 'first = p_dict.get(\'first\', None)\n last = p_dict.get(\'last\', None)'
            elif solution.startswith('7_'):
                df.at[index, 'code'] = 'name = first + " " + last'
            elif solution.startswith('8_'):
                df.at[index, 'code'] = 'name = first + " " + last'
                df.at[index, 'distractor block'] = 'name = first + last'
            elif solution.startswith('9_'):
                df.at[index, 'code'] = 'name_list.append(name)'
            elif solution.startswith('10_'):
                df.at[index, 'code'] = 'return name_list'
        
        elif problem_name == 'Count_Target_In_Range_Order' and (study == 'wn20' or study == 'wn21'):
            if solution.startswith('0_'):
                df.at[index, 'code'] = 'def countInRange(target, start, end, numList):'
            elif solution.startswith('1_') and not solution.startswith('10_') and not solution.startswith('11_'):
                df.at[index, 'code'] = 'count = 0'
            elif solution.startswith('2_'):
                df.at[index, 'code'] = 'count = 0'
                df.at[index, 'distractor block'] = 'count = 1'
            elif solution.startswith('3_'):
                df.at[index, 'code'] = 'for index in range(start, end+1):'
            elif solution.startswith('4_'):
                df.at[index, 'code'] = 'for index in range(start, end+1):'
                df.at[index, 'distractor block'] = 'for index in range(start, end):'
            elif solution.startswith('5_'):
                df.at[index, 'code'] = 'current = numList[index]'
            elif solution.startswith('6_'):
                df.at[index, 'code'] = 'current = numList[index]'
                df.at[index, 'distractor block'] = 'current = numList[start]'
            elif solution.startswith('7_'):
                df.at[index, 'code'] = 'if current == target:'
            elif solution.startswith('8_'):
                df.at[index, 'code'] = 'if current == target:'
                df.at[index, 'distractor block'] = 'if index == target:'
            elif solution.startswith('9_'):
                df.at[index, 'code'] = 'count = count + 1'
            elif solution.startswith('10_'):
                df.at[index, 'code'] = 'count = count + 1'
                df.at[index, 'distractor block'] = 'count++'
            elif solution.startswith('11_'):
                df.at[index, 'code'] = 'return count'
        
        elif problem_name == 'Total_Dict_Values_PP' and (study == 'wn20' or study == 'wn21'):
            if solution.startswith('0_'):
                df.at[index, 'code'] = 'def total_values(dict):'
            elif solution.startswith('1_'):
                df.at[index, 'code'] = 'def total_values(dict):'
                df.at[index, 'distractor block'] = 'def total_values():'
            elif solution.startswith('2_'):
                df.at[index, 'code'] = 'total = 0'
            elif solution.startswith('3_'):
                df.at[index, 'code'] = 'for key in dict:'
            elif solution.startswith('4_'):
                df.at[index, 'code'] = 'for key in dict:'
                df.at[index, 'distractor block'] = 'for key in dict'
            elif solution.startswith('5_'):
                df.at[index, 'code'] = 'total += dict[key]'
            elif solution.startswith('6_'):
                df.at[index, 'code'] = 'total += dict[key]'
                df.at[index, 'distractor block'] = 'total += key'
            elif solution.startswith('7_'):
                df.at[index, 'code'] = 'return total'
   
    df['step name'] = df.loc[:, 'code']

    # Save the modified DataFrame as a new Excel file.
    df.to_excel(output_file_path, index=False)

    print(f"Reformatted data saved to {output_file_path}")

input_file_path = '/Users/cchmagyar/Desktop/results.xlsx'
output_file_path = '/Users/cchmagyar/Desktop/results w code.xlsx'
getcode(input_file_path, output_file_path)
#%%



# Step 2.1 - Add code to solution with indentation.
def getcode(input_file_path, output_file_path):
    # Read the Excel file into a DataFrame.
    df = pd.read_excel(input_file_path)

    # Create a new column called 'Fixed Selection w/ Desried Indentation Level' and set it to empty string.
    df['Fixed Selection w/ Desried Indentation Level'] = ''

    # Iterate over each row and populate the 'code' column based on conditions.
    for index, row in df.iterrows():
        problem_name = row['Problem Name']
        step = str(row['Step Name'])
        
        # This code is specific to the problem and solution that starts with the first number in the solution.
        # For example, '3' in '3_1'. 
        # The first number '3' is the line number in the solution and the second number '1' is indentation (4 spaces in Python).
        if problem_name == 'exp1_pp1a_wn20':
            if step == 'def has22(nums):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'def has22(nums): @indent_0'
            elif step == 'i = 1':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'i = 1 @indent_1'
            elif step == 'while i < len(nums):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'while i < len(nums): @indent_1'
            elif step == 'if nums[i] == 2 and nums[i-1] == 2:':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'if nums[i] == 2 and nums[i-1] == 2: @indent_2'
            elif step == 'return True':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'return True @indent_3'
            elif step == 'i += 1':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'i += 1 @indent_2'
            elif step == 'return False':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'return False @indent_1'
        
        elif problem_name == 'exp1_pp1a_wn21':
            if step == 'def has22(nums):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'def has22(nums): @indent_0'
            elif step == 'for i in range(len(nums)-1):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'for i in range(len(nums)-1): @indent_1'
            elif step == 'if nums[i] == 2 and num[i+1] == 2:':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'if nums[i] == 2 and num[i+1] == 2: @indent_2'
            elif step == 'return True':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'return True @indent_3'
            elif step == 'return False':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'return False @indent_1'
        
        elif problem_name == 'exp1_pp3':
            if step == 'def diffMaxMin(nums):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'def diffMaxMin(nums): @indent_0'
            elif step == 'large = max(nums)\n small = min(nums)':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'large = max(nums)\\n small = min(nums) @indent_1'
            elif step == 'large = max(nums)':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'large = max(nums) @indent_1'
            elif step == 'small = min(nums)':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'small = min(nums) @indent_1'
            elif step == 'return large - small':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'return large - small @indent_1'
        
        elif problem_name == 'exp1_q5_pp':
            if step == 'def get_names(list_of_dict):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'def get_names(list_of_dict): @indent_0'
            elif step == 'name_list = []':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'name_list = [] @indent_1'
            elif step == 'for p_dict in list_of_dict:':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'for p_dict in list_of_dict: @indent_1'
            elif step == 'first = p_dict.get(\'first\', \'Unknown\')\\n last = p_dict.get(\'last\', \'Unknown\')':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'first = p_dict.get(\'first\', \'Unknown\')\\n last = p_dict.get(\'last\', \'Unknown\') @indent_2'
            elif step == 'name = first + " " + last':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'name = first + " " + last @indent_2'
            elif step == 'name_list.append(name)':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'name_list.append(name) @indent_2'
            elif step == 'return name_list':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'return name_list @indent_1'
        
        elif problem_name == 'Count_Target_In_Range_Order':
            if step == 'def countInRange(target, start, end, numList):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'def countInRange(target, start, end, numList): @indent_0'
            elif step == 'count = 0':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'count = 0 @indent_1'
            elif step == 'for index in range(start, end+1):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'for index in range(start, end+1): @indent_1'
            elif step == 'current = numList[index]':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'current = numList[index] @indent_2'
            elif step == 'if current == target:':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'if current == target: @indent_2'
            elif step == 'count = count + 1':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'count = count + 1 @indent_3'
            elif step == 'return count':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'return count @indent_1'
        
        elif problem_name == 'Total_Dict_Values_PP':
            if step == 'def total_values(dict):':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'def total_values(dict): @indent_0'
            elif step == 'total = 0':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'total = 0 @indent_1'
            elif step == 'for key in dict:':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'for key in dict: @indent_1'
            elif step == 'total += dict[key]':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'total += dict[key] @indent_2'
            elif step == 'return total':
                df.at[index, 'Fixed Selection w/ Desried Indentation Level'] = 'return total @indent_1'

    # Save the modified DataFrame as a new Excel file.
    df.to_excel(output_file_path, index=False)

    print(f"Reformatted data saved to {output_file_path}")

input_file_path = '/Users/cchmagyar/Desktop/results.xlsx'
output_file_path = '/Users/cchmagyar/Desktop/fixed selection.xlsx'
getcode(input_file_path, output_file_path)



#%%
# Step 3 - Add ouctomes based on indentation. If the solution is 0_0-1_1-3_1-4_2-6_3-8_2-9_1, then if 0_0-1_0 is submitted, 1_0 would be incorrect.
def getoutcomes(input_file_path, output_file_path):
    # Read the Excel file into a DataFrame.
    df = pd.read_excel(input_file_path)

    # Create a new 'outcome' column.
    df['outcome'] = ''

    # Iterate over each row and update the 'outcome' column based on conditions.
    for index, row in df.iterrows():
        problem_name = row['problem name']
        solution = str(row['solution'])
        study = row['study']
        
        if not pd.isna(solution) and solution.strip() != '':
            
            # 0_0-1_1-3_1-4_2-6_3-8_2-9_1
            if problem_name == 'exp1_pp1a' and study == 'wn20':
                if solution == '0_0' or solution == '1_1' or solution == '3_1' or solution == '4_2' or solution == '6_3' or solution == '8_2' or solution == '9_1':
                    df.at[index, 'outcome'] = 'correct'
                else:
                    df.at[index, 'outcome'] = 'incorrect'

            # 0_0-1_1-3_2-5_3-7_1
            elif problem_name == 'exp1_pp1a' and study == 'wn21':
                if solution == '0_0' or solution == '1_1' or solution == '3_2' or solution == '5_3' or solution == '7_1':
                    df.at[index, 'outcome'] = 'correct'
                else:
                    df.at[index, 'outcome'] = 'incorrect'
            
            # 0_0-2_3_1-4_1
            elif problem_name == 'exp1_pp3' and (study == 'wn20' or study == 'wn21'):
                if solution == '0_0' or solution == '2_3_1' or solution == '2_1' or solution == '3_1' or solution == '4_1':
                    df.at[index, 'outcome'] = 'correct'
                else:
                    df.at[index, 'outcome'] = 'incorrect'
            
            # 0_0-1_1-2_1-3_4_2-7_2-9_2-10_1
            elif problem_name == 'exp1_q5_pp' and (study == 'wn20' or study == 'wn21'):
                if solution == '0_0' or solution == '1_1' or solution == '2_1' or solution == '3_4_2' or solution == '7_2' or solution == '9_2' or solution == '10_1':
                    df.at[index, 'outcome'] = 'correct'
                else:
                    df.at[index, 'outcome'] = 'incorrect'
            
            # 0_0-1_1-3_1-5_2-7_2-9_3-11_1
            elif problem_name == 'Count_Target_In_Range_Order' and (study == 'wn20' or study == 'wn21'):
                if solution == '0_0' or solution == '1_1' or solution == '3_1' or solution == '5_2' or solution == '7_2' or solution == '9_3' or solution == '11_1':
                    df.at[index, 'outcome'] = 'correct'
                else:
                    df.at[index, 'outcome'] = 'incorrect'
            
            # 0_0-2_1-3_1-5_2-7_1
            elif problem_name == 'Total_Dict_Values_PP' and (study == 'wn20' or study == 'wn21'):
                if solution == '0_0' or solution == '2_1' or solution == '3_1' or solution == '5_2' or solution == '7_1':
                    df.at[index, 'outcome'] = 'correct'
                else:
                    df.at[index, 'outcome'] = 'incorrect'

    # Save the modified DataFrame as a new Excel file.
    df.to_excel(output_file_path, index=False)

    print(f"Reformatted data saved to {output_file_path}")

input_file_path = '/Users/cchmagyar/Desktop/results w code.xlsx'
output_file_path = '/Users/cchmagyar/Desktop/results w outcomes.xlsx'
getoutcomes(input_file_path, output_file_path)
#%%





#%%
# Step 5 - Add KC Model Example 1.





#%%
# Step 6 - Add 'Problem Start Time' column to the Excel file.
def update_problem_start_time(input_file_path, output_file_path):
    # Read Excel file into a DataFrame
    df = pd.read_excel(input_file_path)

    # Initialize variables
    prev_event = ''
    prev_correct_incorrect = ''

    # Update 'Problem Start Time', 'Attempt At Step', and 'Is Last Attempt' columns
    for i in range(len(df)):
        event = df.loc[i, 'event']

        if event == 'start':
            df.loc[i:, 'problem start time'] = df.loc[i, 'timestamp']
            df.loc[i:, 'attempt at step'] = 1

        elif event == 'reset':
            df.loc[i:, 'problem start time'] = df.loc[i, 'timestamp']
            df.loc[i:, 'attempt at step'] += 1

        elif any(keyword in event for keyword in ['removedDistractor', 'combinedBlocks', 'removedIndentation']):
            prev_event = df.loc[i - 1, 'event']
            if prev_event in ['incorrect', 'correct']:
                df.loc[i:, 'problem start time'] = df.loc[i, 'timestamp']
                df.loc[i:, 'attempt at step'] += 1

        elif event == 'move':
            prev_event = df.loc[i - 1, 'event']
            if any(keyword in prev_event for keyword in ['removedDistractor', 'combinedBlocks', 'removedIndentation', 'incorrect', 'correct']):
                df.loc[i:, 'problem start time'] = df.loc[i, 'timestamp']
                df.loc[i:, 'attempt at step'] += 1

    # Save the modified DataFrame to a new Excel file
    df.to_excel(output_file_path, index=False)

# Specify the file paths
input_file_path = '/Users/cchmagyar/Desktop/results w outcomes.xlsx'
output_file_path = '/Users/cchmagyar/Desktop/results cleaned i.xlsx'

# Call the function to update the DataFrame and save it as a new Excel file
update_problem_start_time(input_file_path, output_file_path)
#%%



# 1 - Sort the results cleaned ii.xlsx by solution and event.
# 2 - Remove all the empty solution rows that do not have 'removedIndentation' in the 'event' column.



#%%
# Step 7 - Remove duplicate rows from an Excel file.
def remove_duplicate_rows(input_file_path, output_file_path):
    # Read Excel file into a DataFrame
    df = pd.read_excel(input_file_path)

    # Create a set to store unique combinations of solution, problem start time, problem name, and anon student id
    unique_combinations = set()

    # Iterate over the DataFrame rows
    indices_to_drop = []
    for i, row in df.iterrows():
        if row['event'] == 'move':
            combination = (row['solution'], row['problem start time'], row['problem name'], row['anon student id'])
            if combination in unique_combinations:
                indices_to_drop.append(i)
            else:
                unique_combinations.add(combination)

    # Drop the duplicate rows
    df = df.drop(indices_to_drop)

    # Save the modified DataFrame to a new Excel file
    df.to_excel(output_file_path, index=False)

# Specify the file paths
input_file_path = '/Users/cchmagyar/Desktop/results cleaned i.xlsx'
output_file_path = '/Users/cchmagyar/Desktop/results cleaned ii.xlsx'

# Call the function to remove duplicate rows and save the filtered DataFrame as a new Excel file
remove_duplicate_rows(input_file_path, output_file_path)
#%%



# 1 - Remove all the rows with 'move' in the 'event' column.










# Step ?
import re
import pandas as pd

def get_code_from_solution(input_file_path, output_file_path):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(input_file_path)

    # Create a new column 'Fixed Step Name'
    df['Fixed Step Name'] = ''

    # Define a dictionary to map problem names to their corresponding solution and code pairs
    problem_code_mapping = {
        'exp1_pp1a': {
            'wn20': {
                '0_': 'def has22(nums):',
                '1_': 'i = 1',
                '3_': 'while i < len(nums):',
                '4_': 'if nums[i] == 2 and nums[i-1] == 2:',
                '6_': 'return True',
                '8_': 'i += 1',
                '9_': 'return False',
            },
            'wn21': {
                '0_': 'def has22(nums):',
                '1_': 'for i in range(len(nums)-1):',
                '3_': 'if nums[i] == 2 and nums[i+1] == 2:',
                '5_': 'return True',
                '7_': 'return False',
            }
        },
        'exp1_pp3': {
            'wn20': {
                '0_': 'def diffMaxMin(nums):',
                '2_3_': 'large = max(nums)\\n small = min(nums)',
                '2_': 'large = max(nums)',
                '3_': 'small = min(nums)',
                '4_': 'return large - small',
            },
            'wn21': {
                '0_': 'def diffMaxMin(nums):',
                '2_3_': 'large = max(nums)\\n small = min(nums)',
                '2_': 'large = max(nums)',
                '3_': 'small = min(nums)',
                '4_': 'return large - small',
            }
        },
        'exp1_q5_pp': {
            'wn20': {
                '0_': 'def get_names(list_of_dict):',
                '1_': 'name_list = []',
                '2_': 'for p_dict in list_of_dict:',
                '3_4_': 'first = p_dict.get(\'first\', \'Unknown\')\\n last = p_dict.get(\'last\', \'Unknown\')',
                '7_': 'name = first + " " + last',
                '9_': 'name_list.append(name)',
                '10_': 'return name_list',
            },
            'wn21': {
                '0_': 'def get_names(list_of_dict):',
                '1_': 'name_list = []',
                '2_': 'for p_dict in list_of_dict:',
                '3_4_': 'first = p_dict.get(\'first\', \'Unknown\')\\n last = p_dict.get(\'last\', \'Unknown\')',
                '7_': 'name = first + " " + last',
                '9_': 'name_list.append(name)',
                '10_': 'return name_list',
            }
        },
        'Count_Target_In_Range_Order': {
            'wn20': {
                '0_': 'def countInRange(target, start, end, numList):',
                '1_': 'count = 0',
                '3_': 'for index in range(start, end+1):',
                '5_': 'current = numList[index]',
                '7_': 'if current == target:',
                '9_': 'count = count + 1',
                '11_': 'return count',
            },
            'wn21': {
                '0_': 'def countInRange(target, start, end, numList):',
                '1_': 'count = 0',
                '3_': 'for index in range(start, end+1):',
                '5_': 'current = numList[index]',
                '7_': 'if current == target:',
                '9_': 'count = count + 1',
                '11_': 'return count',
            }
        },
        'Total_Dict_Values_PP': {
            'wn20': {
                '0_': 'def total_values(dict):',
                '2_': 'total = 0',
                '3_': 'for key in dict:',
                '5_': 'total += dict[key]',
                '7_': '',
            },
            'wn21': {
                '0_': 'def total_values(dict):',
                '2_': 'total = 0',
                '3_': 'for key in dict:',
                '5_': 'total += dict[key]',
                '7_': '',
            }
        }
    }

    # Iterate over each row and populate the 'Fixed Step Name' column based on conditions
    for index, row in df.iterrows():
        fix = row['Fix']
        outcome = row['Outcome']
        problem_name = row['Problem Name']
        study = row['Study']
        solution = row['Solution']

        if fix == 'Y' and outcome in ('CORRECT', 'INCORRECT'):
            code_mapping = problem_code_mapping.get(problem_name, {}).get(study)
            if code_mapping is not None:
                fixed_step_name = ''
                solution_parts = re.findall(r'\d+_', solution)
                print(solution_parts)
                for part in solution_parts:
                    code = code_mapping.get(part)
                    if code is not None:
                        fixed_step_name += code
                        if part != solution_parts[-1]:
                            fixed_step_name += '\\n '

                df.at[index, 'Fixed Step Name'] = fixed_step_name.strip()

    # Save the modified DataFrame as a new Excel file
    df.to_excel(output_file_path, index=False)
    print(f"Modified data saved to {output_file_path}")

input_file_path = '/Users/cchmagyar/Desktop/results cleaned iii.xlsx'
output_file_path = '/Users/cchmagyar/Desktop/results cleaned iv.xlsx'
get_code_from_solution(input_file_path, output_file_path)










#%%
# Step 8 -
def process_file(input_file_path, output_file_path):
    # Load the Excel file
    df = pd.read_excel(input_file_path)

    # Sort the dataframe by 'Anon Student Id', 'Problem Name', and 'Problem Start Time'
    df = df.sort_values(by=['anon student id', 'problem name', 'problem start time'])

    # Add 'Attempt At Step' column
    df['attempt at step'] = df.groupby(['anon student id', 'problem name'])['problem start time'].transform(lambda x: (~x.duplicated()).cumsum())

    # Add 'Is Last attempt' column
    df['is last attempt'] = df.groupby(['anon student id', 'problem name'])['attempt at step'].transform(lambda x: (x == x.max()).astype(int))

    # If a problem is attempted only once by a student, it should be considered as the last attempt
    df.loc[df.groupby(['anon student id', 'problem name'])['attempt at step'].transform('count') == 1, 'is last attempt'] = 1

    # Add 'Move' column
    df['move'] = df['solution'].notna().groupby([df['anon student id'], df['problem name']]).cumsum().apply(lambda x: 'move ' + str(x) if x > 0 else '')

    # Save the dataframe to a new Excel file
    df.to_excel(output_file_path, index=False)

# Specify the file paths
input_file_path = '/Users/cchmagyar/Desktop/results cleaned ii delete move.xlsx'
output_file_path = '/Users/cchmagyar/Desktop/results cleaned iii.xlsx'
process_file(input_file_path, output_file_path)
# %%