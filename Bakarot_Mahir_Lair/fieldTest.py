import pandas as pd
import os
import numpy as np
source_file = r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\גופי סמך\נתיבי איילון\מהיר לעיר\בקרות שטח\07-בדיקות\טפסי בדיקה\בקרות שטח מהיר לעיר.xlsx'
output_file_path=r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\גופי סמך\נתיבי איילון\מהיר לעיר\בקרות שטח\07-בדיקות\תוצאות בדיקה'
stpos_file_path = r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\gtfs\israel-public-transportation\stops.txt'
stops_data=r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\תיקיות אישיות\אביחי\טופס ריכוז תחנות ראשי - עותק עבודה.xlsx'
elemants_data=r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\גופי סמך\נתיבי איילון\מהיר לעיר\בקרות שטח\02 - אפיון דרישות\קובץ שדות מדידה בקרת הצבה_29082024.xlsx'
output_file= "תוצאות בדיקות"
keywords = ['תקין', 'לא תקין', 'לא נבדק']
joined_df=pd.read_excel(source_file)
df_stops = pd.read_csv(stpos_file_path)
df_stops_data=pd.read_excel(stops_data,skiprows=5)
df_elemants=pd.read_excel(elemants_data)
def stationNameByMakat(makat):
    # Filter the DataFrame to find the row with the specified stop code and retrieve the stop name
    result = df_stops.loc[df_stops['stop_code'] == makat, 'stop_name'].values

    if len(result) > 0:
        stop_name = result[0]  # Get the stop name from the first element of the array
        return stop_name
    else:
            return ''
    # Join DataFrames
# joined_df = pd.concat(df, axis=0, ignore_index=True)
if 'תקינות אורך סככה בפועל בשטח' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('אורך סככה בפועל בשטח') + 1,'תקינות אורך סככה בפועל בשטח',"")
if 'תקינות רוחב סככה' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('רוחב סככה מדיד בשטח') + 1,'תקינות רוחב סככה',"")
if 'תקינות מרחק נגישות דופן ימנית' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('מרחק נגישות דופן ימנית') + 1, 'תקינות מרחק נגישות דופן ימנית',"")
if 'תקינות מרחק נגישות דופן שמאלית' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('מרחק נגישות דופן שמאלית') + 1, 'תקינות מרחק נגישות דופן שמאלית',"")
if 'תקינות מרחק בטיחות אחורי דופן ימין' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('מרחק בטיחות אחורי דופן ימין') + 1, 'תקינות מרחק בטיחות אחורי דופן ימין',"")
if 'תקינות מרחק בטיחות אחורי דופן שמאל' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('מרחק בטיחות אחורי דופן שמאל') + 1, 'תקינות מרחק בטיחות אחורי דופן שמאל',"")
if 'תקינות גובה ספסל חוץ ריהוט רחוב' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('גובה ספסל חוץ ריהוט רחוב') + 1, 'תקינות גובה ספסל חוץ ריהוט רחוב',"")
if 'תקינות גובה ספסל הישענות ריהוט רחוב' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('גובה ספסל הישענות ריהוט רחוב') + 1, 'תקינות גובה ספסל הישענות ריהוט רחוב',"")

if 'תקינות גובה ספסל ישיבה בסככה' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('גובה ספסל ישיבה בסככה') + 1, 'תקינות גובה ספסל ישיבה בסככה',"")
if 'תקינות גובה ספסל הישענות בסככה' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('גובה ספסל הישענות בסככה') + 1, 'תקינות גובה ספסל הישענות בסככה',"")
# Add 'שם תחנה' column if it does not exist
if 'שם תחנה' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('מקט תחנה') + 1, 'שם תחנה',
                     joined_df['מקט תחנה'].apply(lambda x: stationNameByMakat(x)))

# Convert 'שעת התחלה' to datetime
joined_df['שעת התחלה'] = pd.to_datetime(joined_df['שעת התחלה'])
joined_df['שעת השלמה'] = pd.to_datetime(joined_df['שעת השלמה'])
if 'זמן ביצוע בדקות' not in joined_df.columns:
    joined_df.insert(joined_df.columns.get_loc('שעת השלמה') + 1, 'זמן ביצוע בדקות',((joined_df['שעת השלמה'] - joined_df['שעת התחלה']).dt.total_seconds() / 60).round(1))
# Sort by 'שעת התחלה'
joined_df = joined_df.sort_values(by='שעת התחלה')
joined_df = joined_df.fillna("")
for index, row in joined_df.iterrows():
    specific_row = df_stops_data.loc[df_stops_data["מקט תחנה"] == row["מקט תחנה"]]
    specific_project=df_elemants.loc[df_elemants["פרויקט"] == "מהיר לעיר"]
    if row["סוג בקרה"]=="לאחר הצבה":
        print(specific_row["4 מ' 2.45"].values[0])
        print(type(specific_row["4 מ' 2.45"].values[0]))
        if not(pd.isna(specific_row["4 מ' 2.45"].values[0] )):
            if row["אורך סככה בפועל בשטח"]=="4 מטר":
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[1]
            if row["רוחב סככה מדיד בשטח"]== 2.45:
                 joined_df.loc[index,'תקינות רוחב סככה']=keywords[0]
            else:
                joined_df.loc[index,'תקינות רוחב סככה']=keywords[1]
        elif not(pd.isna(specific_row["4 מ' 2.30"].values[0] )):
            if row["אורך סככה בפועל בשטח"]=="4 מטר":
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[1]
            if row["רוחב סככה מדיד בשטח"] == 2.30:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[1]
        elif not(pd.isna(specific_row["4 מ' 2.15"].values[0] )):
            if row["אורך סככה בפועל בשטח"]=="4 מטר":
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[1]
            if row["רוחב סככה מדיד בשטח"] == 2.15:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[1]
        elif not(pd.isna(specific_row["4 מ' צרה (1.70)"].values[0] )):
            if row["אורך סככה בפועל בשטח"]=="4 מטר":
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[1]
            if row["רוחב סככה מדיד בשטח"] == 1.70:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[1]
        elif not(pd.isna(specific_row["8 מ' (2.45)"].values[0] )):
            if row["אורך סככה בפועל בשטח"]=="8 מטר":
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[1]
            if row["רוחב סככה מדיד בשטח"] == 2.45:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[1]
        elif not(pd.isna(specific_row["8 מ' (2.30)"].values[0] )):
            if row["אורך סככה בפועל בשטח"]=="8 מטר":
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[1]
            if row["רוחב סככה מדיד בשטח"] == 2.30:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[1]
        elif not(pd.isna(specific_row["8 מ' (2.15)"].values[0] )):
            if row["אורך סככה בפועל בשטח"]=="8 מטר":
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות אורך סככה בפועל בשטח'] = keywords[1]
            if row["רוחב סככה מדיד בשטח"] == 2.15:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[0]
            else:
                joined_df.loc[index,'תקינות רוחב סככה'] = keywords[1]
        specific_r=specific_project.loc[specific_project["תרגום"]=="מרחק נגישות"].iloc[0]
        if row["מרחק נגישות דופן ימנית"]>=specific_r["מינ"]  :
            joined_df.loc[index,'תקינות מרחק נגישות דופן ימנית'] = keywords[0]
        else:
            joined_df.loc[index,'תקינות מרחק נגישות דופן ימנית'] = keywords[1]
        if row["מרחק נגישות דופן שמאלית"]>=specific_r["מינ"]:
            joined_df.loc[index,'תקינות מרחק נגישות דופן שמאלית'] = keywords[0]
        else:
            joined_df.loc[index,'תקינות מרחק נגישות דופן שמאלית'] = keywords[1]
        specific_r = specific_project.loc[specific_project["תרגום"] == "מרחק בטיחות אחורי"].iloc[0]
        if row["מרחק בטיחות אחורי דופן ימין"] >= specific_r["מינ"] :
            joined_df.loc[index,'תקינות מרחק בטיחות אחורי דופן ימין'] = keywords[0]
        else:
            joined_df.loc[index,'תקינות מרחק בטיחות אחורי דופן ימין'] = keywords[1]
        if row["מרחק בטיחות אחורי דופן שמאל"] >= specific_r["מינ"]:
            joined_df.loc[index,'תקינות מרחק בטיחות אחורי דופן שמאל'] = keywords[0]
        else:
            joined_df.loc[index,'תקינות מרחק בטיחות אחורי דופן שמאל'] = keywords[1]
        specific_r = specific_project.loc[specific_project["תרגום"] == "גובה ספסל"].iloc[0]
        if row["ID"]==42:
            x=4
        if row["גובה ספסל חוץ ריהוט רחוב"] >= specific_r["מינ"] and row["גובה ספסל חוץ ריהוט רחוב"]<=specific_r["מקס"]:
            joined_df.loc[index,'תקינות גובה ספסל חוץ ריהוט רחוב'] = keywords[0]
        else:
            joined_df.loc[index,'תקינות גובה ספסל חוץ ריהוט רחוב'] = keywords[1]
        if row["גובה ספסל ישיבה בסככה"] >= specific_r["מינ"] and row["גובה ספסל ישיבה בסככה"] <= specific_r["מקס"]:
            joined_df.loc[index,'תקינות גובה ספסל ישיבה בסככה'] = keywords[0]
        else:
            joined_df.loc[index,'תקינות גובה ספסל ישיבה בסככה'] = keywords[1]
        specific_r = specific_project.loc[specific_project["תרגום"] == "גובה ספסל הישענות בסככה"].iloc[0]
        if row["גובה ספסל הישענות בסככה"] >= specific_r["מינ"] :
            joined_df.loc[index,'תקינות גובה ספסל הישענות בסככה'] = keywords[0]
        else:
            joined_df.loc[index,'תקינות גובה ספסל הישענות בסככה'] = keywords[1]
        if row["גובה ספסל הישענות ריהוט רחוב"] >= specific_r["מינ"] :
            joined_df.loc[index,'תקינות גובה ספסל הישענות ריהוט רחוב'] = keywords[0]
        else:
            joined_df.loc[index,'תקינות גובה ספסל הישענות ריהוט רחוב'] = keywords[1]
        output_file = os.path.join(output_file_path, 'תוצאות.xlsx')
        # joined_df.to_excel(output_file, index=False)

        # Save to Excel with formatting
        writer = pd.ExcelWriter(os.path.join(output_file_path, output_file), engine='xlsxwriter')
        joined_df.to_excel(writer, sheet_name='Sheet1', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Define format for green and red colors
        green_format = workbook.add_format({'bg_color': 'green', 'font_color': 'white'})
        red_format = workbook.add_format({'bg_color': 'red', 'font_color': 'white'})

        for col_num, col_name in enumerate(joined_df.columns):
            for row_num, value in enumerate(joined_df[col_name]):
                cell_value = str(value)
                if not cell_value.startswith("הערות") and cell_value in keywords:
                    if cell_value == 'תקין':
                        worksheet.write(row_num + 1, col_num, cell_value, green_format)
                    elif cell_value == 'לא תקין':
                        worksheet.write(row_num + 1, col_num, cell_value, red_format)
                    else:
                        worksheet.write(row_num + 1, col_num, cell_value)
                else:
                    worksheet.write(row_num + 1, col_num, cell_value)

        writer._save()




