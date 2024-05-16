from flask import Flask
from flask_cors import CORS
import tensorflow_hub as hub
import tensorflow as tf


def create_flask_app():
    app = Flask(__name__)
    CORS(app, origins="*")
    return app


def load_universal_sentence_encoder():
    model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    sentence_encoder_layer = hub.KerasLayer(model_url, input_shape=[], dtype=tf.string, trainable=False, name="use")
    return sentence_encoder_layer
