# reviewsDownloader
A python script to download app reviews from the google play store

Requires Python >= 3.6 and Node.js >= 6.0.0

Funtions as a Python wrapper around the [https://github.com/facundoolano/google-play-scraper](google-play-scraper) node module.

Handles pause/resume (if terminated, the script will skip any apps for which it has already downloaded reviews when restarted).

## Installation

1. Clone the git repository
2. In the nodeApi folder, unzip the node.zip file
3. In the root folder, run `npm install` to install dependencies

## Usage 

From the root folder run `python downloadReviews.py`

## Parameters

APP_LIST = path to file with list of apps for which reviews must be dowloaded

OUT_FILE = path to file where reviews will be saved

PAGES_FILE = path to a temp file used for pause/resume functionality (probably you don't need to change this)

ERROR_LOG = path to file with log of errors encountered during download

MIN_SLEEP = min sleep time between requests 

MAX_SLEEP = max sleep time between requests

SLEEP = fixed sleep between requests 

LONG_SLEEP = sleep time used when blocked by Google Play

## Troubleshooting

Google Play APIs change often, if the script does not work anymore try running `npm update` from the root folder.
Also check status of possible issues for [https://github.com/facundoolano/google-play-scraper](google-play-scraper) node module. 
