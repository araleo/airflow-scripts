This is a place for my ETL/ELT scripts, currently running on Airflow with data storage on a PostgreSQL AWS database.


Currently running:

Twitter: This project streams tweets directed at Brazil's Supreme Court and it's Justices. Tweets are streamed using tweepy and stored in text files every hour. The airflow DAG parses these text files, and according to the project's rules chooses certain twitter users to score on [Botometer](https://botometer.osome.iu.edu/), figuring out the likelihood that said users are automated accounts. All the parsed info (including several other tweet data) is loaded into the database. A (soon to be build) later stage of this project will feature a web app, which loads the results from the database and shows to visitors tweets directed at each Justice and the likelihood that they come from automated accounts.


G1: Scrapping news articles from G1's website (https://g1.globo.com/), parsing articles to determine if the comment section is opened or closed on each of them (ie if comments are allowed on that specific article), and loading them into the database. Later stages of this project will use NLP to study the differences between news in which comments are allowed or not, and text classification to build a model to classify if the comment section of a certain article will be opened or closed based on the news title and description.


Reddit: Scrapping reddit data using Reddit's API, transforming data according to the projects rules and loading them into the database. The goals of this project are to gather data from different subreddits (thus from different virtual bubbles) and analyse this data to find potential marketing/exposure opportunities in each of these communities. Also to understand how each of theses groups communicate between themselves and each other, understanding what is popular in each bubble and so on. A small sample of the data analysis coming from this project can be found in this [Kaggle notebook](https://www.kaggle.com/araleo/reddit-brasil-data).


Images:

![Twitter Dag Tree View](/screenshots/twitter_dag_tree.png)
![Twitter Dag Gant View](/screenshots/twitter_dag_gant.png)

![Reddit Dag Tree View](/screenshots/reddit_dag_tree.png)
![Reddit Dag Gant View](/screenshots/reddit_dag_gant.png)