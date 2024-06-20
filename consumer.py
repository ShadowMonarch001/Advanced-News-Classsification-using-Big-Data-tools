from kafka import KafkaConsumer
import json
from supabase import create_client

topic_name = 'news_test'
csv_filename = 'consumer_news_output.csv'

# Initialize Kafka consumer
try:
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print("Consumer initialized successfully")

    # Initialize Supabase client
    SUPABASE_URL = "Enter your Supabase url"
    SUPABASE_KEY = "Enter your Supabase key"
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
        # Process messages
        for message in consumer:
            news_article = message.value
            print("Received news article:")
            print("Title:", news_article['title'])
            print("Content:", news_article['content'])
            print("URL:", news_article['url'])
            print("Category:", news_article['category'])
            print()

            # Insert into Supabase table
            response = supabase.table('news').insert([news_article]).execute()

except Exception as e:
    print("Error consuming news:", e)
finally:
    if 'consumer' in locals():
        consumer.close()
