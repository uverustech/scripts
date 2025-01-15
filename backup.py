import os
import tarfile
import subprocess
import dropbox
from datetime import datetime

def tar_zip_directory(project_name, directory, output_dir):
    """Compress a single directory into a tar.gz file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_dir, f"{project_name}_dir_{timestamp}.tar.gz")

    if os.path.exists(directory):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(directory, arcname=os.path.basename(directory))
        print(f"Directory compressed into: {output_filename}")
    else:
        print(f"Warning: Directory {directory} does not exist.")
        return None

    return output_filename

def create_sql_dump(project_name, db_name, output_dir, db_user, db_password):
    """Create an SQL dump file for a single database."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_filename = os.path.join(output_dir, f"{project_name}_db_{db_name}_{timestamp}.sql")
    command = [
        "mysqldump",
        f"--user={db_user}",
        f"--password={db_password}",
        db_name,
    ]
    try:
        with open(dump_filename, "w") as dump_file:
            subprocess.run(command, stdout=dump_file, check=True)
        print(f"SQL dump created: {dump_filename}")
        return dump_filename
    except subprocess.CalledProcessError as e:
        print(f"Error creating SQL dump for database {db_name}: {e}")
        return None

def upload_to_dropbox(file_paths, dropbox_token, dropbox_folder):
    """Upload files to Dropbox in a structured folder format, using upload sessions for large files."""
    dbx = dropbox.Dropbox(dropbox_token)
    CHUNK_SIZE = 100 * 1024 * 1024  # 100 MB

    for file_path in file_paths:
        try:
            file_size = os.path.getsize(file_path)
            target_path = f"{dropbox_folder}/{os.path.basename(file_path)}"

            with open(file_path, "rb") as f:
                if file_size <= CHUNK_SIZE:
                    dbx.files_upload(f.read(), target_path, mode=dropbox.files.WriteMode.overwrite)
                else:
                    upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                    cursor = dropbox.files.UploadSessionCursor(
                        session_id=upload_session_start_result.session_id, offset=f.tell()
                    )
                    commit = dropbox.files.CommitInfo(path=target_path)

                    while f.tell() < file_size:
                        if (file_size - f.tell()) <= CHUNK_SIZE:
                            dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                        else:
                            dbx.files_upload_session_append_v2(f.read(CHUNK_SIZE), cursor)
                            cursor.offset = f.tell()

                print(f"Uploaded {file_path} to Dropbox at {target_path}")
        except Exception as e:
            print(f"Failed to upload {file_path} to Dropbox: {e}")

def main():
    # Configuration
    projects = {
        "joinda": {"dir": "/www/wwwroot/joinda.io", "db": "joinda"},
        
    } 
    output_dir = "/root/backups" 
    db_user = "root" 
    db_password = os.getenv("DB_PASSWORD")
    dropbox_token = os.getenv("DROPBOX_TOKEN")
    dropbox_root_folder = "/backups"

    if not db_password or not dropbox_token:
        print("Error: Missing DB_PASSWORD or DROPBOX_TOKEN environment variables.")
        return

    os.makedirs(output_dir, exist_ok=True)

    for project_name, config in projects.items():
        project_folder = f"{dropbox_root_folder}/{project_name}/{datetime.now().strftime('%Y-%m-%d')}"

        # Step 1: Compress the directory
        tar_file = tar_zip_directory(project_name, config["dir"], output_dir)

        # Step 2: Create SQL dump
        sql_dump = create_sql_dump(project_name, config["db"], output_dir, db_user, db_password)

        # Step 3: Upload to Dropbox
        files_to_upload = [f for f in [tar_file, sql_dump] if f is not None]
        upload_to_dropbox(files_to_upload, dropbox_token, project_folder)

if __name__ == "__main__":
    main()
