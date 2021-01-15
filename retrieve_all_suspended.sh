
cd app
python retrieve.py ab ../raws/upd.ab.md --all-suspended
sleep 1
python retrieve.py qa ../raws/upd.qa.md --all-suspended
