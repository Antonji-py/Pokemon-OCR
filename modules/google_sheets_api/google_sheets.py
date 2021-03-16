import gspread
from oauth2client.service_account import ServiceAccountCredentials


def auth(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("modules/google_sheets_api/credentials.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name).sheet1

    return sheet


def write_data(sheet_name, future):
    sheet = auth(sheet_name)
    data = future.result()

    get_written_rows = sheet.get_all_values()
    current_cell_number = len(get_written_rows) + 1

    update_ordinal = sheet.update_cell(current_cell_number, 1, current_cell_number - 1)
    update_name = sheet.update_cell(current_cell_number, 2, data["name"])
    update_rarity = sheet.update_cell(current_cell_number, 3, data["rarity"])
    update_available_items = sheet.update_cell(current_cell_number, 4, data["available_items"])
    update_lowest_price = sheet.update_cell(current_cell_number, 5, data["lowest_price"])
    update_price_trend = sheet.update_cell(current_cell_number, 6, data["price_trend"])
    update_average_price_30 = sheet.update_cell(current_cell_number, 7, data["average_price_30"])
    update_average_price_7 = sheet.update_cell(current_cell_number, 8, data["average_price_7"])
    update_average_price_1 = sheet.update_cell(current_cell_number, 9, data["average_price_1"])
