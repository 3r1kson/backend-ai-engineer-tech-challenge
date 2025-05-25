import json
from sklearn.metrics import classification_report
from nltk.translate.bleu_score import sentence_bleu

from src.app.services.conversation_manager_service import ConversationManager
from src.app.models.message_model import MessageModel

class Evaluator:
    def __init__(self, conversation_manager: ConversationManager):
        self.conversation_manager = conversation_manager

    def load_dataset(self, path: str):
        with open(path, "r") as f:
            return json.load(f)

    def evaluate(self, dataset_path: str):
        dataset = self.load_dataset(dataset_path)

        y_true_intents = []
        y_pred_intents = []

        bleu_scores = []

        for sample in dataset:
            history = [MessageModel(**msg) for msg in sample["conversation_history"]]
            result = self.conversation_manager.run(history, sample["current_prospect_message"], sample.get("prospect_id"))

            expected_intent = sample["expected"]["intent"]
            predicted_intent = result.reasoning_trace.lower() if "intent" in result.reasoning_trace.lower() else "unknown"

            y_true_intents.append(expected_intent)
            y_pred_intents.append(predicted_intent)

            ref = [sample["expected"]["suggested_response_draft"].split()]
            hyp = result.suggested_response_draft.split()
            bleu = sentence_bleu(ref, hyp)
            bleu_scores.append(bleu)

            print(f"Sample {sample['id']} -> Intent: {predicted_intent}, BLEU: {bleu:.2f}")

        print("\n=== Intent Classification Report ===")
        print(classification_report(y_true_intents, y_pred_intents))
        print(f"\nAvg BLEU score: {sum(bleu_scores)/len(bleu_scores):.2f}")
