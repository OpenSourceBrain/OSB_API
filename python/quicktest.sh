set -e
python project_metadata.py
python CheckModelDB.py
python activity.py 10
python curate.py 10
python retrieveNML2.py 10
