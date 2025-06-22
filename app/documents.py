# documents.py
"""
Script to add multiple documents to MongoDB for the System Chatbot
Run this file to populate your database with sample system information
"""

import sys
import os
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from database.database_manager import DatabaseManager
from config.config import Config

class DocumentInserter:
    def __init__(self):
        self.config = Config()
        self.db_manager = DatabaseManager()
        self.model = SentenceTransformer(self.config.MODEL_NAME)
        print("DocumentInserter initialized successfully!")
    
    def vectorize_text(self, text: str) -> List[float]:
        """Convert text to vector using SBERT"""
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"Vectorization error: {e}")
            return []
    
    def add_single_document(self, command_id: str, command: str, response: str, category: str) -> bool:
        """Add a single document to MongoDB"""
        try:
            # Check if command_id already exists
            existing = self.db_manager.find_by_command_id(command_id)
            if existing:
                print(f"Warning: Command ID '{command_id}' already exists. Skipping...")
                return False
            
            # Vectorize the command
            vector = self.vectorize_text(command)
            if not vector:
                print(f"Error: Failed to vectorize command '{command_id}'")
                return False
            
            # Insert into database
            success = self.db_manager.insert_system_info(
                command_id=command_id,
                command=command,
                response=response,
                category=category,
                vector=vector
            )
            
            if success:
                print(f"✓ Successfully added: {command_id}")
                return True
            else:
                print(f"✗ Failed to add: {command_id}")
                return False
                
        except Exception as e:
            print(f"Error adding document {command_id}: {e}")
            return False
    
    def add_multiple_documents(self, documents: List[Dict]) -> Dict:
        """Add multiple documents to MongoDB"""
        print(f"Starting bulk insert of {len(documents)} documents...")
        
        successful = 0
        failed = 0
        failed_items = []
        
        for doc in documents:
            try:
                success = self.add_single_document(
                    command_id=doc['command_id'],
                    command=doc['command'],
                    response=doc['response'],
                    category=doc['category']
                )
                
                if success:
                    successful += 1
                else:
                    failed += 1
                    failed_items.append(doc['command_id'])
                    
            except Exception as e:
                print(f"Error processing document: {e}")
                failed += 1
                failed_items.append(doc.get('command_id', 'unknown'))
        
        result = {
            'total_attempted': len(documents),
            'successful': successful,
            'failed': failed,
            'failed_items': failed_items
        }
        
        print(f"\n=== BULK INSERT RESULTS ===")
        print(f"Total attempted: {result['total_attempted']}")
        print(f"Successful: {result['successful']}")
        print(f"Failed: {result['failed']}")
        if failed_items:
            print(f"Failed items: {failed_items}")
        print("===========================\n")
        
        return result

# ============== SAMPLE DOCUMENTS ==============
# Add your documents here
SYSTEM_DOCUMENTS = [
    {
        "command_id": "restart_server",
        "command": "how to restart the server",
        "response": "To restart the server, run the following command: sudo systemctl restart apache2",
        "category": "server_management"
    },
    {
        "command_id": "check_disk_space",
        "command": "check disk space",
        "response": "To check disk space, use: df -h",
        "category": "system_monitoring"
    },
    {
        "command_id": "view_system_logs",
        "command": "how to view system logs",
        "response": "To view system logs, run: tail -f /var/log/syslog",
        "category": "troubleshooting"
    },
    {
        "command_id": "check_memory_usage",
        "command": "check memory usage",
        "response": "To check memory usage, use: free -h",
        "category": "system_monitoring"
    },
    {
        "command_id": "restart_service",
        "command": "restart a service",
        "response": "To restart a specific service, run: sudo systemctl restart <service_name>",
        "category": "service_management"
    },
    {
        "command_id": "check_cpu_usage",
        "command": "check cpu usage",
        "response": "To check CPU usage, run: top or htop",
        "category": "system_monitoring"
    },
    {
        "command_id": "backup_database",
        "command": "how to backup database",
        "response": "To backup MySQL database, run: mysqldump -u username -p database_name > backup.sql",
        "category": "database_management"
    },
    {
        "command_id": "check_network_connectivity",
        "command": "check network connectivity",
        "response": "To check network connectivity, run: ping google.com",
        "category": "network_troubleshooting"
    },
    {
        "command_id": "list_running_processes",
        "command": "list running processes",
        "response": "To list running processes, use: ps aux | grep <process_name>",
        "category": "process_management"
    },
    {
        "command_id": "check_firewall_status",
        "command": "check firewall status",
        "response": "To check firewall status, run: sudo ufw status",
        "category": "security"
    },
    {
        "command_id": "update_system",
        "command": "update system packages",
        "response": "To update system packages, run: sudo apt update && sudo apt upgrade",
        "category": "system_maintenance"
    },
    {
        "command_id": "check_port_usage",
        "command": "check which ports are in use",
        "response": "To check port usage, run: netstat -tulpn",
        "category": "network_troubleshooting"
    },
    {
        "command_id": "create_user",
        "command": "create new user",
        "response": "To create a new user, run: sudo adduser <username>",
        "category": "user_management"
    },
    {
        "command_id": "change_file_permissions",
        "command": "change file permissions",
        "response": "To change file permissions, use: chmod <permissions> <filename>",
        "category": "file_management"
    },
    {
        "command_id": "find_large_files",
        "command": "find large files",
        "response": "To find large files, run: find / -type f -size +100M 2>/dev/null",
        "category": "file_management"
    }
]

# ============== ADDITIONAL DOCUMENT SETS ==============
# You can add more document sets here

SERVER_MANAGEMENT_DOCS = [
    {
        "command_id": "nginx_restart",
        "command": "restart nginx server",
        "response": "To restart nginx, run: sudo systemctl restart nginx",
        "category": "web_server"
    },
    {
        "command_id": "apache_restart",
        "command": "restart apache server",
        "response": "To restart apache, run: sudo systemctl restart apache2",
        "category": "web_server"
    },
    {
        "command_id": "check_nginx_config",
        "command": "check nginx configuration",
        "response": "To check nginx config, run: sudo nginx -t",
        "category": "web_server"
    }
]

DATABASE_DOCS = [
    {
        "command_id": "mysql_start",
        "command": "start mysql service",
        "response": "To start MySQL service, run: sudo systemctl start mysql",
        "category": "database"
    },
    {
        "command_id": "postgres_backup",
        "command": "backup postgresql database",
        "response": "To backup PostgreSQL, run: pg_dump dbname > backup.sql",
        "category": "database"
    },
    {
        "command_id": "mysql_user_create",
        "command": "create mysql user",
        "response": "To create MySQL user, run: CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';",
        "category": "database"
    }
]

# ============== MAIN EXECUTION ==============
def main():
    """Main function to run the document insertion"""
    try:
        print("=== System Chatbot Document Inserter ===")
        print("Initializing...")
        
        inserter = DocumentInserter()
        
        print("\nChoose an option:")
        print("1. Insert sample system documents (15 documents)")
        print("2. Insert server management documents (3 documents)")
        print("3. Insert database documents (3 documents)")
        print("4. Insert all documents (21 documents)")
        print("5. Insert custom documents (modify the CUSTOM_DOCS list)")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            result = inserter.add_multiple_documents(SYSTEM_DOCUMENTS)
        elif choice == "2":
            result = inserter.add_multiple_documents(SERVER_MANAGEMENT_DOCS)
        elif choice == "3":
            result = inserter.add_multiple_documents(DATABASE_DOCS)
        elif choice == "4":
            all_docs = SYSTEM_DOCUMENTS + SERVER_MANAGEMENT_DOCS + DATABASE_DOCS
            result = inserter.add_multiple_documents(all_docs)
        elif choice == "5":
            # Add your custom documents here
            CUSTOM_DOCS = [
                {
                    "command_id": "custom_command_1",
                    "command": "your custom command",
                    "response": "your custom response",
                    "category": "custom_category"
                }
                # Add more custom documents here
            ]
            result = inserter.add_multiple_documents(CUSTOM_DOCS)
        else:
            print("Invalid choice. Exiting...")
            return
        
        if result['successful'] > 0:
            print(f"✓ Successfully inserted {result['successful']} documents!")
        else:
            print("✗ No documents were inserted.")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

def add_custom_document(command_id: str, command: str, response: str, category: str):
    """Helper function to add a single custom document"""
    try:
        inserter = DocumentInserter()
        success = inserter.add_single_document(command_id, command, response, category)
        return success
    except Exception as e:
        print(f"Error adding custom document: {e}")
        return False

def clear_all_documents():
    """WARNING: This will delete ALL documents from the collection"""
    try:
        inserter = DocumentInserter()
        confirm = input("Are you sure you want to delete ALL documents? Type 'YES' to confirm: ")
        if confirm == "YES":
            # This would require adding a method to database_manager.py
            print("Clear function not implemented. Add to database_manager.py if needed.")
        else:
            print("Operation cancelled.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

# ============== USAGE EXAMPLES ==============
"""
USAGE EXAMPLES:

1. Run the script directly:
   python documents.py

2. Import and use specific functions:
   from documents import DocumentInserter, add_custom_document
   
   # Add a single document
   add_custom_document("test_cmd", "test command", "test response", "test")
   
   # Use the class for more control
   inserter = DocumentInserter()
   inserter.add_multiple_documents([...])

3. Add your own documents:
   - Modify the CUSTOM_DOCS list in the main() function
   - Or create your own document list and pass it to add_multiple_documents()

4. Document format:
   {
       "command_id": "unique_identifier",
       "command": "user query or command",
       "response": "system response or instruction",
       "category": "category_name"
   }
"""