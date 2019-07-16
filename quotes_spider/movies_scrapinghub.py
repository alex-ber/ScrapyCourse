from scrapinghub import ScrapinghubClient
import csv
import time
import pandas as pd

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
        itemsDataFrame = pd.DataFrame()
        for item_aggelia in job.items.iter():
            # Save all items (dictionaries) to the DataFrame
            itemsDataFrame = itemsDataFrame.append(item_aggelia, ignore_index=True)
        movie_name = 'results/' + itemsDataFrame.MOVIE_NAME[0].replace(' ', '_') + '.json'
        itemsDataFrame.to_json(movie_name)
        # # Delete job from ScrapingHub
        # logger.debug("Deleting job " + job_key_name)
        # job.delete()

def run_jobs():
    with open('filename.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i,row in enumerate(reader):
            if i%10 == 0:
                time.sleep(1800)
            title = row[0] + ' movie'
            job = spider.jobs.run(units=2, job_args={'movie_name': title}, add_tag=[title.replace(' ','_')])
            print(job)

if __name__ == "__main__":
    run_jobs()
    #get_items()