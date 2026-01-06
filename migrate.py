import os

# The directory where your archive folders currently live
ARCHIVE_DIR = os.path.join(os.getcwd(), "CCL_Archive")

def migrate_year_folders():
    # Get all items in the archive directory
    items = os.listdir(ARCHIVE_DIR)
    
    for item in items:
        item_path = os.path.join(ARCHIVE_DIR, item)
        
        # Only process if it's a directory and exactly 2 characters long
        if os.path.isdir(item_path) and len(item) == 2:
            try:
                # Determine the century
                year_int = int(item)
                
                if 91 <= year_int <= 99:
                    new_year = f"19{item}"
                elif 0 <= year_int <= 25:
                    new_year = f"20{item.zfill(2)}"
                else:
                    continue # Skip anything outside our range
                
                new_path = os.path.join(ARCHIVE_DIR, new_year)
                
                print(f"Renaming: {item} -> {new_year}")
                os.rename(item_path, new_path)
                
            except ValueError:
                # Skip folders that aren't numeric
                continue

if __name__ == "__main__":
    migrate_year_folders()
