# create_dummy_files.py

import os
from pathlib import Path

# --- Configuration ---
ROOT_FOLDER = Path(os.getcwd())

# Define files to create with simple dummy content
FILES_TO_CREATE = {
    # New Decoy Files (High-Value Targets)
    "API_Keys_Internal.json": '{"live_api_key": "DECOY_KEY_DO_NOT_USE", "db_password": "DECOY_PASSWORD_123"}',
    "CEO_Contract.docx": "This is a decoy document acting as a high-value executive contract.",
    "Client_Records.csv": "ID,Name,Email\n1,Decoy Client,decoy@example.com\n",
    
    # Ensuring Existing Files Exist (if they were accidentally deleted)
    "Finance_Report_Q3.xlsx": "This is the decoy finance report file.",
    "Employee_List.xlsx": "Real employee data here.",
    
    # Adding content to two existing simple files to ensure they're up-to-date
    "meeting_transcript.txt": "Meeting Notes: Project X kickoff. Attendees: John, Jane. Status: On track.",
    "server_log_2025-10.log": "LOG: 10/09/2025 - Initializing Watcher. Status: OK.",
}

# --- Execution ---
def create_files():
    print("--- Creating/Updating Dummy Files ---")
    
    for filename, content in FILES_TO_CREATE.items():
        file_path = ROOT_FOLDER / filename
        
        # NOTE: For .docx and .xlsx, we create simple text files. 
        # The file extension is enough for the Watcher to classify the risk.
        if filename.endswith(('.docx', '.xlsx')):
            try:
                # For Office files, write simple text. The file size will be small, but the name is high-value.
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Created/Updated text content for: {filename}")
            except Exception as e:
                print(f"Error writing {filename}: {e}")
        else:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Created/Updated: {filename}")
            except Exception as e:
                print(f"Error writing {filename}: {e}")
                
    print("\nFile creation complete. Total files: 18 (excluding directories and logs)")

if __name__ == "__main__":
    create_files()