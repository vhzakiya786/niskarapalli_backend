import pygsheets
import pandas as pd


def fn_update_google_sheet(instance):
    
    # Authorization for Google Sheets API
    gc = pygsheets.authorize(service_file='google_key/drivekey.json')

    # Open Google Sheet
    sh = gc.open('niskarapalli_app')
    wks = sh[0]
    # Check if the record already exists in the spreadsheet
    df = wks.get_as_df()
    
    
   

    # Define the headers
    headers = [
        'id', 'name', 'mobile', 'offer', 'offer_description', 'year',
        'upi_id1', 'upi_id2', 'upi_id3', 'upi_id4', 'jan', 'feb', 'march',
        'april', 'may', 'june', 'july', 'august', 'september', 'october',
        'november', 'december'
    ]

    # If DataFrame is empty, create the header row
    if df.empty:
        wks.update_row(1, headers)
        df = pd.DataFrame(columns=headers)  # Update the DataFrame with headers

    # Prepare the data to be inserted/updated
    record_data = {
        'id': instance.id,
        'name': instance.name,
        'mobile': instance.mobile,
        'offer': instance.offer,
        'offer_description': instance.offer_description,
        'year': instance.year,
        'upi_id1': instance.upi_id1,
        'upi_id2': instance.upi_id2,
        'upi_id3': instance.upi_id3,
        'upi_id4': instance.upi_id4,
        'jan': float(instance.jan  or 0),
        'feb': float(instance.feb or 0),
        'march': float(instance.march or 0),
        'april': float(instance.april or 0),
        'may': float(instance.may or 0),
        'june': float(instance.june or 0),
        'july': float(instance.july or 0),
        'august': float(instance.august or 0),
        'september': float(instance.september or 0),
        'october': float(instance.october or 0),
        'november': float(instance.november or 0),
        'december': float(instance.december or 0),
    }

    # Check if the record already exists in the DataFrame
    row_index = df.index[df['id'] == instance.id].tolist()

    # If the record exists, update it
    if row_index:
        for column, value in record_data.items():
            wks.update_value((row_index[0] + 2, df.columns.get_loc(column) + 1), value)
    else:
        # If the record doesn't exist, append a new row
        wks.append_table(values=list(record_data.values()))
