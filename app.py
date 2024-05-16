from flask import Flask, request, jsonify
import numpy as np
import joblib
import pandas as pd
from database import create_db_engine
from settings import create_flask_app, load_universal_sentence_encoder

# Load the model
model = joblib.load('model.pkl')


# Create the Flask app
app = create_flask_app()

# Load the Universal Sentence Encoder model
sentence_encoder_layer = load_universal_sentence_encoder()

# This line creates a connection to the database
engine = create_db_engine()


@app.route('/')
def index():
    return 'Hello, World!'


# Define the POST route
@app.route('/recommend', methods=['POST'])
def recommend_papers():
    # Get the search term from the request
    search_term = request.json['search_term']

    # Embed the search term
    search_embedding = sentence_encoder_layer([search_term])

    # Get the nearest neighbors
    distances, indices = model.kneighbors(np.array(search_embedding).reshape(1, -1))

    # Convert indices to a list
    indices = [int(i) for i in indices[0]]
    indices = str(indices).replace('[', '').replace(']', '')

    # Create the SQL query
    query = "SELECT * FROM papers WHERE id IN ({})".format(indices)

    # Execute the query and get the results as a DataFrame
    df = pd.read_sql(query, engine)

    # return the results as array of dictionaries
    response = df.to_dict(orient='records')

    return response


# Run the Flask app
if __name__ == '__main__':
    app.run()
