import joblib
from typing import List
from thesis_classifier.helper.preprocess import Preprocess
from pathlib import Path

path = Path(__file__).parent/'models/sklearn_MNB_2.model'


class Classifier:
    def __init__(self):
        self.model = joblib.load(path)
        self.preprocess = Preprocess().list

    def predicts(self, inputs: List[str]):
        predicted_list = self.preprocess(inputs)
        predicted_tf = self.model.tf.transform(predicted_list)
        predicted_data = self.model.predict(predicted_tf)
        return predicted_data
