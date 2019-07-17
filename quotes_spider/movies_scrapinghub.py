from scrapinghub import ScrapinghubClient
import csv
import time
import pandas as pd
import json

apikey = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
client = ScrapinghubClient(apikey)
project = client.get_project(111111)
spider = project.spiders.get('spidername')

def get_items():
    jobs_summary = project.jobs.iter(state='finished')
    job_keys = [j['key'] for j in jobs_summary]
    for job_key in job_keys:
        # Get the corresponding job from the key, as "job"
        job = project.jobs.get(job_key)
        # Create an empty list that will store all items (dictionaries)
        items=[]
        for item_aggelia in job.items.iter():
            # Save all items (dictionaries) to the list
            items.append(item_aggelia)
        movie_name = 'results/new/' + job.metadata.get('tags')[0]
        with open(movie_name, 'w') as f:
            json.dump(items, f)
        # # Delete the job from ScrapingHub
        # logger.debug("Deleting job " + job_key_name)
        # job.delete()


def run_jobs():
    with open('titles.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            if i % 10 == 0 and i != 0:
                time.sleep(1800)
            title = row[0] + ' movie'
            job = spider.jobs.run(units=2, job_args={'movie_name': title}, add_tag=[title.replace(' ', '_')])
            print(job)


def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file, )
        for d in data:
            movie_name = d['MOVIE_NAME']
            url = d['URL']
            text = d['TEXT']
            # get line by line from text
            for line in text.splitlines():
                print(line)


if __name__ == '__main__':
    # run_jobs()
    get_items()

