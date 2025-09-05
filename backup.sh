#!/bin/bash

# ===============================
# Config
# ===============================
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DB_FILE="$SCRIPT_DIR/db.sqlite3"
BACKUP_NAME="db-backup__$(date '+%F__%H-%M').db"
FTP_SERVER="backup.henrik-petersen.de"
FTP_USER="backup-admin"
FTP_PASS="O172?3zeu"
EMAIL_RECIPIENT="henrik@petersen-digital.de"

LOG_FILE="$SCRIPT_DIR/backup_$(date '+%F__%H-%M').log"

# ===============================
# Start Backup
# ===============================
echo "===== Database Backup started =====" | tee "$LOG_FILE"

# Prüfen, ob Datenbank existiert
if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file $DB_FILE not found!" | tee -a "$LOG_FILE"
    exit 1
fi

# Backup erstellen
if cp "$DB_FILE" "$SCRIPT_DIR/$BACKUP_NAME"; then
    echo "Database copied successfully: $BACKUP_NAME" | tee -a "$LOG_FILE"
else
    echo "Error: Failed to copy database!" | tee -a "$LOG_FILE"
    exit 1
fi

# ===============================
# FTP Upload
# ===============================
echo "Uploading $BACKUP_NAME to FTP server..." | tee -a "$LOG_FILE"

ftp -inv "$FTP_SERVER" <<EOF >> "$LOG_FILE" 2>&1
user $FTP_USER $FTP_PASS
binary
put $BACKUP_NAME
bye
EOF

if [ $? -eq 0 ]; then
    echo "FTP upload successful!" | tee -a "$LOG_FILE"
else
    echo "Error: FTP upload failed!" | tee -a "$LOG_FILE"
fi

# ===============================
# Cleanup
# ===============================
rm -f "$BACKUP_NAME"
echo "Local backup file removed." | tee -a "$LOG_FILE"

# ===============================
# Send Email
# ===============================
if command -v mail >/dev/null 2>&1; then
    mail -s "Database Backup Log $(date '+%F %H:%M')" "$EMAIL_RECIPIENT" < "$LOG_FILE"
    echo "Backup log sent to $EMAIL_RECIPIENT" | tee -a "$LOG_FILE"
else
    echo "Warning: 'mail' command not found. Cannot send email." | tee -a "$LOG_FILE"
fi

echo "===== Backup Completed =====" | tee -a "$LOG_FILE"