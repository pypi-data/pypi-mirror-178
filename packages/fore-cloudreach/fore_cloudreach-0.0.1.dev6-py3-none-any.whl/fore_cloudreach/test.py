
from __future__ import print_function

import os.path
import datetime
import fore_cloudreach as fc 


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Ni5B7zolPKD2J0CXQSaLec31AXw8HpcdM_xPJKPILRw' #'1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Rechnung!F5:G8'

def read_test(spreadsheet_id):
    """ Show basic usage of the Sheets API.
        Prints values from a sample spreadsheet
    """
    authet = fc.Auth() 
    creds = authet.get()

    if creds is None:
        raise Exception("invalid user authentication")
        return

    if spreadsheet_id == '':
        spd_id = input("Enter the Google Sheet file ID from the URL:\n")
        spreadsheet_id = spd_id 

    print("currentDir: ", format(os.getcwd()))

    tmp = fc.Template(template_id=spreadsheet_id)
    print(f"processing file id: {tmp.id} ...")

    month_year = datetime.datetime.now().strftime('%m-%Y')
    resp = tmp.new_from_template(creds, spreadsheet_id, month_year)
    print("\n\n\nresp:\n\n", format(resp))