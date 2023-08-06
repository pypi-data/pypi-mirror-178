
from fore_cloudreach.errors import ReadingMapFileError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Template:
    """
    The `Template` class will represent Google Sheets template used to create and feed GS report file with prepared data data.
    """

    id = ""

    def __init__(self, template_id) -> None:
        if template_id == "":
            raise Exception("The template id is required")
            return
        self.id = template_id


    def new_from_template(self, creds, spreadsheet_id, report_name) -> object:
        """ **Duplicates** the first tab sheet of the given template object
            This must be called before ingesting the monthly report data for each customer.
            It will return the new tab sheet id the is required for the ingestion process.
        """

        requests = []
        requests.append({
            # Duplicates the contents of a sheet. # Duplicates a sheet.
            "duplicateSheet": { 
                # The zero-based index where the new sheet should be inserted. The index of all sheets after this are incremented.
                "insertSheetIndex": 1,
                # If set, the ID of the new sheet. If not set, an ID is chosen. If set, the ID must not conflict with any existing sheet ID. If set, it must be non-negative. 
                "newSheetId": None, 
                # The name of the new sheet. If empty, a new name is chosen for you.
                "newSheetName": report_name, 
                # The sheet to duplicate. If the source sheet is of DATA_SOURCE type, its backing DataSource is also duplicated and associated with the new copy of the sheet. No data execution is triggered, the grid data of this sheet is also copied over but only available after the batch request completes.
                "sourceSheetId": 0,
            } 
        })

        # API docs: https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.html#batchUpdate
        try:

            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API for duplicating the first sheet (index=0) of the spreadsheet
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id, 
                body={'requests':requests}
                ).execute()
            
            # TODO[dev]: extract the sheetId from the response object!

            # The `response` object sample:
            # {'spreadsheetId': '1Ni5B7zolPKD2J0CXQSaLec31AXw8HpcdM_xPJKPILRw', 
            #  'replies': [
            #     {'duplicateSheet': 
            #        {'properties': {'sheetId': 431392078, 'title': '11-2022', 'index': 1, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}}]}
            return response

        except HttpError as err:
            print("new_from_template threw an error:", format(err))
            return


    def read_map(self, creds, readrange) -> list:
        """ *read_map* will read a specific `hardcoded` range of the mapping file

            This method is a tiny functioanlity (nearlly hard-coded) to read the mapping between
            each customer and its spreadsheet ID for the file with this customer's finance report.

            The current functionality will stop reading the mapped rows as sson as it finds
            an empty value in a cell in `column A`, even if there are more rows with values in that column,
            or the last row from the given range is reached.

            Modify this method in order to apply different logic.\n\n

            Keyword arguments:\n
            creds     -- authentication credentials\n
            readrange -- the range where the mapping is stored\n
        """
    
        try:
            service = build('sheets', 'v4', credentials=creds)
            
            # Call the Sheets API
            sheet = service.spreadsheets()

            result = sheet.values().get(spreadsheetId=self.id,
                                        range=readrange).execute()

            values = result.get('values', [])

            if not values:
                print('No data found.')
                return None

            range_width = len(values[0])
            map_titles = []
            cstmmap = []

            for idx, row in enumerate(values):
                
                if idx == 0:
                    for i in range(range_width):
                        map_titles.append(row[i])
                    continue
                
                map_row = []
                for j in range(range_width):
                    map_row.append(row[j])

                cstmmap.append(map_row)
            
            return cstmmap

        except HttpError as err:
            print(f"HTTP error: {err}", err)
            raise ReadingMapFileError(str(err.content))