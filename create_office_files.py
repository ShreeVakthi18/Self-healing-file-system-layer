# create_office_files.py (FINAL, FINAL UPDATE for more critical extensions)

import os
from pathlib import Path
from docx import Document
from openpyxl import Workbook
import json
import csv
import zipfile

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
    
    # --- NEW CRITICAL CONFIG/EMAIL EXTENSIONS ---
    "server_settings.conf": "[Database]\nhost=127.0.0.1\nuser=admin\npassword=DECOY_PASS_123", # .conf
    "app_config.ini": "[Settings]\nversion=2.5\ndebug_mode=False\napi_endpoint=/v1/data", # .ini
    "archived_emails.pst": "This file is a placeholder for a large, confidential Outlook email archive.", # .pst
    
    # --- DATABASE/ARCHIVE/CODE EXTENSIONS ---
    "Production_Users.db": "Database table: Users (ID, Username, Hash). This is dummy database data.",
    "Full_Backup_2025.zip": "This archive is a decoy backup container.",
    "Database_Schema.sql": "CREATE TABLE Users (UserID INT PRIMARY KEY, Username VARCHAR(50));",
    
    # --- WORD/DOCX FILES (Total 10) ---
    "Legal_Settlement_Docs.docx": "Confidential legal documents relating to a recent settlement.",
    "HR_Disciplinary_Records.docx": "Private HR records. Access highly restricted.",
    "Patent_Application_Draft.docx": "Draft of a valuable new patent application.",
    "Executive_Meeting_Summary.docx": "Notes from a private board meeting.",
    "ProjectPlan.docx": "Standard project planning document.",
    "Onboarding_Checklist.docx": "Checklist for new employee setup.",
    "Roadmap_2025.docx": "Product development roadmap.",
    "Company_Policy_Manual.docx": "Internal company usage guidelines.",
    
    # --- EXCEL/XLSX FILES (Total 5) ---
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
    "Employee_List.xlsx": [
        ['Employee ID', 'Name', 'Department'],
        ['EMP-001', 'John Doe', 'HR'],
        ['EMP-002', 'Jane Smith', 'Finance']
    ],
    
    # --- SIMPLE TEXT/LOG FILES ---
    "meeting_transcript.txt": "Meeting Notes: Project X kickoff. Attendees: John, Jane. Status: On track.",
    "server_log_2025-10.log": "LOG: 10/09/2025 - Initializing Watcher. Status: OK.",
}

# --- Dedicated File Creation Functions (No change here) ---

def create_json(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json.loads(content), f, indent=4)

def create_docx(file_path, content):
    document = Document()
    document.add_paragraph(content)
    document.save(file_path)

def create_xlsx(file_path, content_rows):
    workbook = Workbook()
    sheet = workbook.active
    for row in content_rows:
        sheet.append(row)
    workbook.save(file_path)

def create_csv(file_path, content_rows):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(content_rows)

def create_zip(file_path, content):
    # This function is also used for .PST, .DB, .CONF, .INI files as placeholders
    # as they are not standard text files but require simple content for monitoring.
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

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
            elif filename.endswith(('.txt', '.log', '.db', '.sql', '.conf', '.ini', '.pst', '.zip')):
                # Use the create_zip function to create simple placeholder files for all non-standard types
                create_zip(file_path, str(content))
            
            print(f"Successfully created/updated: {filename}")
            
        except Exception as e:
            print(f"Error creating {filename}: {e}")
                
    print("\nFile creation complete. Your project now monitors files with over 10 unique extensions! 🎉")

if __name__ == "__main__":
    create_files()