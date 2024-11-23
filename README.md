# AI-Nutrition



**Project Overview**  
The AI Nutrition Assistant is an innovative solution that simplifies the complexities of meal planning and nutrition management. Designed to help individuals adopt healthier eating habits, this application provides personalized meal recommendations, nutritional information, and recipe guidance. By leveraging the power of AI, the assistant tailors its suggestions based on the user's dietary preferences and goals, making it easier for anyone to make informed and healthy food choices.

---

## Key Features

- **Personalized Meal Recommendations**: Suggests meals based on dietary preferences (e.g., vegan, gluten-free).
- **Nutritional Information**: Provides detailed nutritional data for selected recipes, including calories and macronutrients.
- **Recipe Retrieval**: Filters recipes by meal type (e.g., breakfast, lunch, dinner) and cuisine (e.g., Italian, Mexican).
- **Interactive Q&A**: Offers real-time responses to user queries about nutrition and healthy eating habits.
- **Step-by-Step Cooking Instructions**: Guides users through the preparation process of recipes with clear instructions.

---

## Dataset

The dataset powering the assistant consists of 180 records and 7 key columns:

- **recipe_name**: Name of the recipe
- **ingredients**: List of ingredients used in the recipe
- **nutritional_information**: Nutritional details (calories, macronutrients)
- **dietary_tags**: Tags indicating dietary preferences (e.g., vegan, gluten-free)
- **meal_type**: Type of meal (e.g., breakfast, lunch, dinner)
- **cuisine_type**: Cuisine category (e.g., Italian, Mexican)
- **instructions**: Cooking instructions

The dataset is located in the `data/data.csv` file and was generated using ChatGPT.

---

## Technologies

- **Python 3.11.9**: Core programming language for the application
- **Docker & Docker Compose**: For containerization and application deployment
- **Minsearch**: Full-text search engine for efficient data retrieval
- **Flask**: API interface to interact with the assistant
- **Grafana**: For monitoring and visualization
- **PostgreSQL**: Backend database for storing data
- **OpenAI**: Language Model (LLM) for natural language processing

---

## Running the Application

### 1. **Database Configuration**

Before starting the application for the first time, initialize the database.

- Start PostgreSQL container using Docker Compose:

```bash
docker-compose up postgres
```

- Run the `db_start.py` script to set up the database:

```bash
pipenv shell
cd nutrition_assistant
export POSTGRES_HOST=localhost
python db_start.py
```

### 2. **Running with Docker-Compose**

To run the application using Docker Compose, simply execute:

```bash
docker-compose up
```

### 3. **Running with Docker (Without Compose)**

For debugging or other purposes, you can run the application using Docker without Docker Compose.

1. **Build the Docker image**:

```bash
docker build -t nutrition_assistant .
```

2. **Run the Docker container**:

```bash
docker run -it --rm \
    --network="nutrition-assistant_default" \
    --env-file=".env" \
    -e OPENAI_API_KEY=${OPENAI_API_KEY} \
    -e DATA_PATH="data/data.csv" \
    -p 5000:5000 \
    nutrition_assistant
```

3. **Access the application** at:  
`http://localhost:5000`

### 4. **Making API Requests**

You can make requests to the running application using `curl`.

#### Ask a Question:

```bash
QUESTION="Is the Vegetarian Chili recipe suitable for a vegan diet?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    http://localhost:5000/question
```

#### Provide Feedback:

```bash
FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    http://localhost:5000/feedback
```

---

## Ingestion and Data Processing

The ingestion script, `ingest.py`, is used for processing and loading the data into the system. It leverages **Minsearch** for full-text search functionality.

---

## Experimentation and Evaluation

We conducted several experiments using Jupyter notebooks to evaluate the performance of the AI Nutrition Assistant. Key experiments and metrics include:

- **RAG Flow and Evaluation**: Analyzing how well the system provides relevant answers and recommendations.
- **Data Generation**: Generating the ground truth dataset for evaluating the retrieval system.

### Evaluation Metrics

- **Retrieval Evaluation**:
    - Hit Rate: 97%
    - Mean Reciprocal Rank (MRR): 91%
    - Improved Version:
        - Hit Rate: 97%
        - MRR: 95%

- **RAG Flow Evaluation**:
    - Using the **LLM-as-a-Judge** metric:
        - 95% Relevant
        - 5% Partly Relevant

---

## Monitoring

Currently, the monitoring setup is a work-in-progress using **Grafana** for system health and performance metrics.

---

## Future Work

- Further optimization of the recommendation algorithm
- Enhanced monitoring and alerting
- Expanded dataset for more diverse meal suggestions
- Integration with third-party APIs for real-time nutrition tracking

