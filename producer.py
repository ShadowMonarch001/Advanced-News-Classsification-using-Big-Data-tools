from newsapi import NewsApiClient
from kafka import KafkaProducer
from json import dumps
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
import os

os.environ['PYSPARK_PYTHON'] = r'/path/to/python'

# Create a SparkSession
spark = SparkSession.builder \
    .appName("NewsAPI to Kafka") \
    .getOrCreate()

# Define categories
label_dict = {
 'POLITICS':0.0,
 'ENTERTAINMENT':1.0,
 'WORLD NEWS':2.0,
 'QUEER VOICES':3.0,
 'COMEDY':4.0,
 'BLACK VOICES':5.0,
 'SPORTS':6.0,
 'MEDIA':7.0,
 'WOMEN':8.0,
 'WEIRD NEWS':9.0,
 'CRIME':10.0,
 'BUSINESS':11.0,
 'LATINO VOICES':12.0,
 'IMPACT':13.0,
 'RELIGION':14.0,
 'TRAVEL':15.0,
 'STYLE':16.0,
 'GREEN':17.0,
 'PARENTS':18.0,
 'TECH':20.0,
 'HEALTHY LIVING':21.0,
 'SCIENCE':22.0,
 'EDUCATION':23.0,
 'TASTE':24.0,
 'ARTS & CULTURE':25.0,
 'COLLEGE':26.0
}

# Kafka settings
kafka_topic = 'news_test'
kafka_servers = ['localhost:9092']

# Initialize News API client
newsapi = NewsApiClient(api_key='Enter your News API key here')

# Load a saved PipelineModel object
pipeline_model = PipelineModel.load("mypipeline")

try:
    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers=kafka_servers,api_version=(0,11,5),
                             request_timeout_ms=1200000,
                             value_serializer=lambda x: dumps(x).encode('utf-8'))
    print("Kafka producer initialized successfully")

    # Fetch top headlines
    top_headlines = newsapi.get_top_headlines(language='en', category='general', page_size=20)

    # Send top headlines to Kafka
    for article in top_headlines['articles']:
        title = article['title']
        content = article['content']
        
        if content:
            prediction_test = pipeline_model.transform(spark.createDataFrame([(title,)], ['description']))
            category = int(prediction_test.select('prediction').collect()[0][0])
            
            category_term = next((key for key, value in label_dict.items() if value == category), None)
            
            news_data = {
                'title': title,
                'content': content,
                'url': article['url'],
                'category': category_term if category_term else category
            }
            producer.send(kafka_topic, value=news_data)
            producer.flush()
            

except Exception as e:
    print("Error fetching or sending news:", e)
finally:
    try:
        producer.close()
    except Exception as close_error:
        print("Error closing Kafka producer:", close_error)

