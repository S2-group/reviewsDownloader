import subprocess
from subprocess import CalledProcessError
import csv
from time import sleep
import json

APP_LIST = "../app_annie_scraper/apps_no_dups.csv"
OUT_FILE = "reviews/reviews.csv"
PAGES_FILE = "reviews/pages.csv"
ERROR_LOG = "reviews_error_log.txt"
MIN_SLEEP = 5
MAX_SLEEP = 5
SLEEP = 5
LONG_SLEEP = 300
CSV_NULL_VALUE = ""
MAX_PAGE = 111
separator = "$%$"


def write_error_log(_apk_package, _page, exception, _error_log):
    with open(_error_log, 'a+') as log_file:
        log_file.write("Error while downloading reviews for app " + _apk_package
                       + " at page" + str(_page)
                       + " reason: " + str(exception.__cause__) + "\n")
        log_file.flush()
        log_file.close()


def request_reviews(_apk_package, _page):
    try:
        output = subprocess.check_output(["./nodeApi/node","nodeApi/singleRevRequest.js", _apk_package.strip(), str(_page).strip()])
    except CalledProcessError as ce:
        return []
    if len(output) <= 2:
        print("No reviews!")
        raise Exception
    temp = output.decode('utf8').split("\n")
    reviews = []
    for line in temp:
        if len(line) > 0:
            reviews.append(line)
    return reviews


print("Initializing set of pages already downloaded")
# retrieve the last page we downloaded for each app
last_pages = dict()
with open(PAGES_FILE) as pages:
    p_reader = csv.DictReader(pages, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    for line in p_reader:
        last_pages.update({line['app_name']: line['page']})

print("Initializing set of reviews already downloaded")
# retrieve the ids of the apps we already downloaded
downloaded_ids = set()
with open(OUT_FILE) as downloaded_reviews:
    r_reader = csv.DictReader(downloaded_reviews, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    for review in r_reader:
        downloaded_ids.add(review['id'])


with open(APP_LIST) as app_list, open(OUT_FILE, "a+") as out_file, open(PAGES_FILE, "a+") as p_file:
    app_reader = csv.DictReader(app_list, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    pages_writer = csv.DictWriter(out_file, delimiter=';', quoting=csv.QUOTE_MINIMAL, fieldnames=['app_name', 'page'])
    review_writer = csv.DictWriter(out_file, delimiter=';', quoting=csv.QUOTE_MINIMAL,
                                   fieldnames=['id', 'userName', 'date', 'url', 'score', 'title', 'text'])
    for line in app_reader:
        page = last_pages.get(line['package_name'])

        try:
            if page is None:
                page = 0
            page = int(page)

            if page >= MAX_PAGE:
                continue

            has_more = True
            while has_more:
                if page >= MAX_PAGE:
                    has_more = False

                print("Requesting page {} of app {}".format(page, line['package_name']))
                reviews = request_reviews(line['package_name'], page)
                for review in reviews:
                    review_dict = json.loads(review)
                    if review_dict['id'] not in downloaded_ids:
                        del review_dict['userImage']
                        review_writer.writerow(review_dict)
                        out_file.flush()
                        downloaded_ids.add(review_dict['id'])
                if len(reviews) == 0:
                    print("I have been blocked! I will sleep for {} seconds".format(LONG_SLEEP))
                    sleep(LONG_SLEEP)
                elif page >= MAX_PAGE or len(reviews) < 40:
                    print("Retrieved last reviews for {}".format(line['package_name']))
                    review_writer.writerow({'package_name': line['package_name'], 'page': page})
                    p_file.flush()
                    has_more = False
                else:
                    page += 1
                    print("Sleep for {} seconds".format(SLEEP))
                    sleep(SLEEP)

        except Exception as e:
            print(e)
            has_more = False
            write_error_log(line['package_name'], page, e, ERROR_LOG)
