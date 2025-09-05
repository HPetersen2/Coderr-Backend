echo "Database Backup started"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BACKUP_NAME="db-backup__$(date '+%F__%H-%M').db"
cp "$SCRIPT_DIR/db.sqlite3" "$BACKUP_NAME"
echo "Uploading file:  $BACKUP_NAME"

echo "
 verbose
 open backup.henrik-petersen.de
 user backup-admin 'O172?3zeu'
 binary
 put $BACKUP_NAME
 bye
" | ftp -n > ftp_$$.log
echo "Backup successful"

rm $BACKUP_NAME
rm ftp_$$.log