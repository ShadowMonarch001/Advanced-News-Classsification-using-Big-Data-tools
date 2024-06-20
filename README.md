
# Advanced News Classification using Big Data Tools

## Project Overview

In today's information age, efficiently categorizing and organizing the vast amount of news generated daily is a significant challenge. Leveraging big data technologies, this project addresses scalability, accuracy, and relevance in news categorization. The system has applications across various domains including stock market analysis, personalized content delivery, recommendation systems, trend analysis, and ad placement.

## How It Works

1. **Data Preprocessing and Model Training with PySpark**
   - Preprocess the news data.
   - Train a classification model using PySpark.
   - Save the trained model for future predictions.

2. **Kafka Setup**
   - Deploy Kafka on Docker containers on an EC2 instance.
   - Create Kafka topics for communication between producer and consumer.

3. **Producer Application**
   - Fetch news via an API.
   - Load the saved PySpark model.
   - Predict the category of the news.
   - Send the news along with its category to a Kafka topic.

4. **Consumer Application**
   - Consume news messages from the Kafka topic.
   - Store the news and its category in an online database (Supabase).

5. **Online Database**
   - Set up a PostgreSQL database on Supabase.
   - Create a table with specified columns to store the news data.(do it before running the producer.py)

6. **Visualization**
   - Use Metabase, running on Docker, to visualize the stored news data.

7. **Dockerization and Deployment**
   - Dockerize each component (Producer, Consumer, Database).
   - Use Docker Compose to orchestrate the deployment.
   - Deploy the Docker containers on EC2 instances.
     ![image](https://github.com/ShadowMonarch001/Advanced-News-Classsification-using-Big-Data-tools/assets/129870255/08ecbff4-cc82-4fe1-8e08-bbc7244c844c)


## Prerequisites

- AWS Account
- Docker and Docker Compose installed
- Supabase Account
- News API Account (e.g., NewsAPI)

## Setup Instructions

### Supabase

1. Sign up for a [Supabase](https://supabase.io/) account.
2. Create a new project.
3. Navigate to the SQL editor and create a table with the following columns:
   ```sql
   CREATE TABLE news (
       id SERIAL PRIMARY KEY,
       title TEXT,
       description TEXT,
       url TEXT,
       category TEXT,
       published_at TIMESTAMP
   );
   ```
   ![image](https://github.com/ShadowMonarch001/Advanced-News-Classsification-using-Big-Data-tools/assets/129870255/dd1394c3-a152-45bf-ba0f-b942b6ceff3c)


### AWS

1. Sign up for an [AWS](https://aws.amazon.com/) account.
2. Launch an EC2 instance with Docker installed.

### Docker

1. Ensure Docker and Docker Compose are installed on your local machine or EC2 instance.
2. Clone the GitHub repository:
   ```sh
   git clone https://github.com/ShadowMonarch001/Advanced-News-Classsification-using-Big-Data-tools.git
   cd Advanced-News-Classsification-using-Big-Data-tools
   ```

### News API

1. Sign up for a [NewsAPI](https://newsapi.org/) account.
2. Obtain your API key for fetching news.

### Running the Project

1. **Configure Environment Variables**:
   Create a `.env` file in the project root directory and add the following variables:
   ```env
   NEWS_API_KEY=<your_news_api_key>
   SUPABASE_URL=<your_supabase_url>
   SUPABASE_KEY=<your_supabase_key>
   ```

2. **Start Kafka with Docker Compose**:
   ```sh
   docker-compose up -d
   ```

3. **Run Producer**:
   ```sh
   python producer.py
   ```

4. **Run Consumer**:
   ```sh
   python consumer.py
   ```

### Visualization with Metabase

1. **Run Metabase with Docker**:
   - Pull the Metabase Docker image:
     ```sh
     docker pull metabase/metabase
     ```
   - Run the Metabase container:
     ```sh
     docker run -d -p 3000:3000 --name metabase metabase/metabase
     ```
   - Access Metabase at `http://<your-ec2-instance-ip>:3000` and complete the setup.

2. **Connect Metabase to Supabase**:
   - In Metabase, add a new database connection.
   - Choose PostgreSQL and enter your Supabase connection details.
   - Start creating dashboards and visualizations based on your news data.
![image](https://github.com/ShadowMonarch001/Advanced-News-Classsification-using-Big-Data-tools/assets/129870255/47497ce4-47a6-4108-b6b5-fbc0fce17559)

