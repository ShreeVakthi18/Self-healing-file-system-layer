# create_office_files.py (UPDATED to add 4 more .xlsx files)

import os
from pathlib import Path
from docx import Document
from openpyxl import Workbook
import json
import csv

# --- Configuration ---
ROOT_FOLDER = Path(os.getcwd())

# Define files to create with simple dummy content
FILES_TO_CREATE = {
    # --- DECOY FILES ---
    "API_Keys_Internal.json": '{"live_api_key": "DECOY_KEY_DO_NOT_USE", "db_password": "DECOY_PASSWORD_123"}',
    "CEO_Contract.docx": "This is a decoy document acting as a high-value executive contract. An attacker would prioritize modifying or deleting this file.",
    "Client_Records.csv": [
        ['ID', 'Name', 'Email', 'Status'],
        ['101', 'Decoy Client A', 'decoy.a@honeypot.com', 'Active'],
        ['102', 'Decoy Client B', 'decoy.b@honeypot.com', 'Inactive']
    ],
    "Finance_Report_Q3.xlsx": [
        ['Quarter', 'Revenue', 'Status'],
        ['Q3-2025', '£5.2M', 'Decoy Data']
    ],
    
    # --- NEW REAL/HIGH-VALUE .XLSX FILES (4 additional files) ---
    "Q4_Budget_Forecast.xlsx": [
        ['Month', 'Projected', 'Actual'],
        ['Oct', '£100k', '£95k'],
        ['Nov', '£120k', '£125k']
    ],
    "Server_Inventory.xlsx": [
        ['Asset Tag', 'Location', 'Status'],
        ['SV-001', 'Data Center A', 'Online'],
        ['SV-002', 'Data Center B', 'Maintenance']
    ],
    "Vendor_Payment_Schedules.xlsx": [
        ['Vendor', 'Amount', 'Date'],
        ['Acme Corp', '$5,000', '11/01/2025'],
        ['Beta Inc', '$2,500', '11/15/2025']
    ],
    "User_Access_Log.xlsx": [
        ['User', 'System', 'Last Login'],
        ['Admin', 'Core DB', '2025-10-09'],
        ['Guest', 'Web Portal', '2025-10-08']
    ],
    
    # --- EXISTING REAL FILES ---
    "Employee_List.xlsx": [
        ['Employee ID', 'Name', 'Department'],
        ['EMP-001', 'John Doe', 'HR'],
        ['EMP-002', 'Jane Smith', 'Finance']
    ],
    "meeting_transcript.txt": "Meeting Notes: Project X kickoff. Attendees: John, Jane. Status: On track.",
    "server_log_2025-10.log": "LOG: 10/09/2025 - Initializing Watcher. Status: OK.",
}

# --- Dedicated File Creation Functions (No change here) ---

def create_json(file_path, content):
    """Creates a properly formatted JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json.loads(content), f, indent=4)

def create_docx(file_path, content):
    """Creates an openable .docx file using python-docx."""
    document = Document()
    document.add_paragraph(content)
    document.save(file_path)

def create_xlsx(file_path, content_rows):
    """Creates an openable .xlsx file using openpyxl."""
    workbook = Workbook()
    sheet = workbook.active
    for row in content_rows:
        sheet.append(row)
    workbook.save(file_path)

def create_csv(file_path, content_rows):
    """Creates a proper CSV file."""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(content_rows)

# --- Execution ---
def create_files():
    print("--- Creating/Updating Formatted Files ---")
    
    for filename, content in FILES_TO_CREATE.items():
        file_path = ROOT_FOLDER / filename
        
        try:
            if filename.endswith('.docx'):
                create_docx(file_path, content)
            elif filename.endswith('.xlsx'):
                create_xlsx(file_path, content)
            elif filename.endswith('.json'):
                create_json(file_path, content)
            elif filename.endswith('.csv'):
                create_csv(file_path, content)
            elif filename.endswith(('.txt', '.log')):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            print(f"Successfully created/updated: {filename}")
            
        except Exception as e:
            print(f"Error creating {filename}: {e}")
                
    print("\nFile creation complete. You can now open the new files.")

if __name__ == "__main__":
    create_files()