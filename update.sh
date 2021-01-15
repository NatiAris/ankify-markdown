
cd app
python update.py ../raws/upd.ab.md
sleep 1
python update.py ../raws/upd.qa.md

git add ../raws/past
git add ../raws/csv
git commit -m "Update cards"
git push

cd backup
./make_backup.sh

