
from django.db.models.signals import post_save
from django.dispatch import receiver

from home_app.helpers import fn_update_google_sheet
from home_app.models import UserModel


@receiver(post_save, sender=UserModel)
def update_google_sheet(sender, instance, **kwargs):
    pass
    print('signals')
    print(instance.__dict__)
    fn_update_google_sheet(instance)
    # import pygsheets
    # import pandas as pd
    # #authorization
    # gc = pygsheets.authorize(service_file='google_key/drivekey.json')

    # # Create empty dataframe
    # df = pd.DataFrame()

    # # Create a column
    # df['name'] = ['aymen', 'Steve', 'Sarah']

    # #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    # sh = gc.open('niskarapalli_app')

    # #select the first sheet 
    # wks = sh[0]

    # #update the first sheet with df, starting at cell B2. 
    # wks.set_dataframe(df,(1,1))