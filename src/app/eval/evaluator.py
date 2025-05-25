# python
import json
from typing import List, Dict
from sklearn.metrics import precision_recall_fscore_support
from sklearn.preprocessing import MultiLabelBinarizer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# app
from src.app.models.process_message_request_model import ProcessMessageRequestModel
from src.app.services.conversation_manager_service import ConversationManager
from src.app.services.message_service import process_incoming_message


class Evaluator:
    def __init__(self, conversation_manager: ConversationManager):
        self.conversation_manager = conversation_manager

    def load_golden_dataset(self, dataset_path: str) -> List[Dict]:
        with open(dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate(self, dataset_path: str, knowledge: str):
        data = self.load_golden_dataset(dataset_path)

        total_samples = len(data)
        correct_intent = 0
        correct_sentiment = 0
        total_bleu = 0.0
        correct_action = 0

        true_entities_list = []
        pred_entities_list = []

        smoothie = SmoothingFunction().method4

        for sample in data:
            expected = sample["expected"]

            request_data = ProcessMessageRequestModel(
                conversation_history=sample["conversation_history"],
                current_prospect_message=sample["current_prospect_message"],
                prospect_id=sample["prospect_id"]
            )

            actual_response = process_incoming_message(request_data)
            actual_json = json.loads(actual_response.body)

            try:
                if "data" not in actual_json or "classification" not in actual_json["data"]:
                    print(f"❌ Skipping sample due to malformed response: {actual_json}")
                    continue

                classification = actual_json["data"]["classification"]
                intent = classification.get("intent")
                sentiment = classification.get("sentiment")
                entities = classification.get("entities", [])
                internal_next_steps = actual_json["data"].get("internal_next_steps", [])
                suggested_response = actual_json["data"].get("suggested_response_draft", "")

            except Exception as e:
                print(f"❌ Error processing sample: {e}")
                continue

            if intent == expected["intent"]:
                correct_intent += 1

            if sentiment == expected["sentiment"]:
                correct_sentiment += 1

            bleu = sentence_bleu(
                [expected["suggested_response_draft"].split()],
                suggested_response.split(),
                smoothing_function=smoothie
            )
            total_bleu += bleu

            true_entities_list.append(set(expected.get("entities", [])))
            pred_entities_list.append(set(entities))

            expected_actions = set(step["action"] for step in expected.get("internal_next_steps", []))
            actual_actions = set(step["action"] for step in internal_next_steps)
            if expected_actions == actual_actions:
                correct_action += 1

        mlb = MultiLabelBinarizer()
        y_true = mlb.fit_transform(true_entities_list)
        y_pred = mlb.transform(pred_entities_list)

        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='micro', zero_division=0
        )

        print("------ Evaluation Results ------")
        print(f"Total Samples: {total_samples}")
        print(f"Intent Accuracy: {correct_intent / total_samples:.2f}")
        print(f"Sentiment Accuracy: {correct_sentiment / total_samples:.2f}")
        print(f"Entity Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.2f}")
        print(f"Average BLEU Score: {total_bleu / total_samples:.2f}")
        print(f"Action Accuracy: {correct_action / total_samples:.2f}")
        print("--------------------------------")
