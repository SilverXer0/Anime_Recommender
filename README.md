This is an anime recommendation system based on myanimelist. Thus, it requires an account on this website with previous anime 
watched/selected in order to make a recommendation. 

This application aims to reduce time needed to scroll through myanimelist.net to find an anime to watch and instead will give 
a machine learning recommendation based on previously watched shows from your account. The idea is as follows:

1. The user enters their myanimelist.net user ID
2. The app shows 5 random animes from the top 20 generated recommendations based on shows the user has previously watched 

The project consists of 5 parts: 

1. Crawl Scheduler
2. Crawler
3. Data Ingestion + ETL
4. Machine Learning Pipelines
5. Web App (Frontend)

Crawl scheduler: A job that when called will fetch a list of anime/profile urls from a database and push them to a message queue. The crawl schedulers are deployed as Cloud Functions, the database as a postgres Cloud SQL database and the message queue as a Pub/Sub topic.

Crawler: Scrapy jobs that pull message urls from the scheduler message queue and crawl them. The crawled data items are pushed to a data ingestion message queue and the crawler jobs also connects to the schedule database to update it. The crawler is deployed to Google Kubernetes Engine and the data ingestion queue is a Pub/Sub topic.

Data Ingestion and ETL: An Apache Beam streaming job pulls data items from the ingestion queue and pushes them to BigQuery in a landing area. An Apache Airflow pipeline is run to aggregate, clean and validate the crawled data into well structured datasets. The new data is saved in BigQuery and Storage. The ingestion beam job is deployed as a Dataflow job and the Apache Airflow ETL pipeline runs in a Cloud Composer environment.

Machine Learning Pipelines: Each pipeline handles both retrieval and ranking steps.
    For retrieval step, the pipeline starts by generating the train/val/test data for retrieval, then trains a retrieval model and finally runs batch inference for retrieval and saves the results.
    For ranking step, the pipeline starts by generating the train/val/test data for ranking, then trains a ranking model and finally runs batch inference for ranking on the retrieved results and saves the final results.
    The pipelines are Kubeflow pipelines and they run on Google VertexAI pipelines. Data is fetched from and saved to both BigQuery and Storage.

Web App: The generated recommendations are ingested into a Redis database and a small Flask web application fetches the recommendations from Redis for each user recommendation request.

Current UI is scrappy, needs work. Hope you enjoy.