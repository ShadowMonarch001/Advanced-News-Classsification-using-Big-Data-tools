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
    SUPABASE_URL = "https://zsmabakfawjhsetabnue.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpzbWFiYWtmYXdqaHNldGFibnVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU0OTY1NjksImV4cCI6MjAzMTA3MjU2OX0.M0tJ7R8ViR_MAax6MB_ru1Nlg_46q6MbgzQ8AfOerqc"
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
