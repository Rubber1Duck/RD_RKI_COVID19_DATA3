from download_pkg import *
import os, json
import datetime as dt
from update_github_action import update
from fallzahlen_update import f_update

def build_meta(datum):
  filename = "RKI_COVID19_XXXX-XX-XX.csv.xz"
  filename = filename.replace("XXXX-XX-XX", datum)
  source_path = "W:\\RKI_COVID19_DATA_Archiv\\" + filename
  dest_path = "F:\\RD_RKI_COVID19_DATA3\\data\\" + filename
  datetime = dt.datetime.strptime(datum, "%Y-%m-%d")
  unix_timestamp = int(dt.datetime.timestamp(datetime)*1000)
  os.system("copy " + source_path + " " + dest_path)

  new_meta = {
    "publication_date": datum,
    "version": datum,
    "size": os.path.getsize(dest_path),
    "filename": filename,
    "url": dest_path,
    "modified": unix_timestamp}
  
  return new_meta
datum = "2020-04-27"
new_meta = build_meta(datum)
metaNew_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataStore", "meta", "meta_new.json")
with open(metaNew_path, "w", encoding="utf8") as json_file:
        json.dump(new_meta, json_file, ensure_ascii=False)
versionsplit = datum.split("-")
datumversion = versionsplit[0] + versionsplit[1] + versionsplit[2]
version = "v1.9." + datumversion
update()
f_update()
meta_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataStore", "meta", "meta.json")
os.remove(meta_path)
os.rename(metaNew_path, meta_path)
os.system("git add .")
os.system('git commit -m"update ' + datumversion + '"')
os.system("git push")
os.system("git tag " + version)
os.system('git push --tag')


