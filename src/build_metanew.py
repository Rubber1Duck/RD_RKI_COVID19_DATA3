from download_pkg import *
import os, json
import datetime as dt
from update_github_action import update
from fallzahlen_update import f_update
import utils as ut

def build_meta(datum):
  filename = "RKI_COVID19_XXXX-XX-XX.csv.xz"
  filename = filename.replace("XXXX-XX-XX", datum)
  source_path = "W:\\RKI_COVID19_DATA_Archiv\\" + filename
  dest_path = "F:\\RD_RKI_COVID19_DATA2\\data\\" + filename
  datetime = dt.datetime.strptime(datum, "%Y-%m-%d")
  unix_timestamp = int(dt.datetime.timestamp(datetime)*1000)
  ut.copy(source=source_path, destination=dest_path)

  new_meta = {
    "publication_date": datum,
    "version": datum,
    "size": os.path.getsize(dest_path),
    "filename": filename,
    "url": dest_path,
    "modified": unix_timestamp}
  
  return new_meta

new_meta = build_meta("2020-04-22")
metaNew_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataStore", "meta", "meta_new.json")
with open(metaNew_path, "w", encoding="utf8") as json_file:
        json.dump(new_meta, json_file, ensure_ascii=False)

update()
f_update()
meta_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataStore", "meta", "meta.json")
os.remove(meta_path)
os.rename(metaNew_path, meta_path)


