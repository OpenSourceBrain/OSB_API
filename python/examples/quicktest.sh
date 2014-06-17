set -e
if [ "$1" == "-a" ]; then
    python project_metadata.py
fi
python CheckModelDB.py
python activity.py 10
python curate.py 10
python retrieveNML2.py 10
python tags.py


