
cd app
python ankify.py ../raws/ab.md
sleep 1
python ankify.py ../raws/qa.md

git add ../raws/past
git add ../raws/csv
git commit -m "Add cards"
git push

cd backup
./make_backup.sh

