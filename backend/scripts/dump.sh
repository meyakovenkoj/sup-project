cd
cd db_dumps
mongodump --archive=dump$(date "+%d%m%y-%H%M%S").gz --gzip --db=sup_data
