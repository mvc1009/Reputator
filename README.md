
# Reputator

Python3 script that scraps mxtoolbox in order to find if a list of IPs are blacklisted. Generates a json output with the results and another script named `parser.py` create a word table with the final parsed results.

## Requirements

```
pip3 install selenium
pip3 install beautifulsoup4
pip3 install python-docx
```

## Usage

```
python3 reputator.py ips.txt out.json
python3 parser.py out.json
```
