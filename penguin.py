import arxiv
import json
import tempfile
import datetime
import pytz
import csv
import os
from google.cloud import storage
from google.oauth2 import service_account
from googletrans import Translator
translator = Translator()




def main():
    dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    dt_old = dt_now - datetime.timedelta(days=3)
    dt_now = dt_now.strftime('%Y%m%d')
    dt_day = dt_old.strftime('%Y%m%d')
    dt_last = dt_now + '115959'
    cv_papers = arxiv.query(query='cat:cs.cv AND submittedDate:[{} TO {}]'.format(dt_day, dt_now), sort_by='submittedDate')
    if len(cv_papers) > 100:
        cv_papers = cv_papers[:100]
    
    cv_all_dict = []
    for i, cv_paper in enumerate(cv_papers):
        id = cv_paper['id']
        title = cv_paper['title']
        pdf = cv_paper['pdf_url']
        summary = cv_paper['summary']
        summary = ''.join(summary.splitlines())
        summary_ja = translator.translate(summary, src='en', dest='ja')
        summary_ja = str(summary_ja.text)
        cv_dict = {"id": id, "title": title, "pdf": pdf, "summary": summary, "summary_ja": summary_ja}
        cv_all_dict.append(cv_dict)
    # print(cv_all_dict)
    # input()

    with tempfile.TemporaryDirectory() as temp_path:
        write_path = temp_path + '/penguin.json'
        with open(write_path, 'w') as f:
            json.dump(cv_all_dict, f, indent=4)
        # with open(write_path, encoding='unicode-escape') as f:
        #     print(f.read())
        #     input()

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=''
        client = storage.Client()
        bucket_name = "penguin-first"
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob('penguin.json')
        blob.upload_from_filename(filename=write_path)



if __name__ == '__main__':
    main()

