# python
import os

# app
from src.app.services.conversation_manager_service import ConversationManager
from src.app.eval.evaluator import Evaluator


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
knowledge_path = os.path.join(BASE_DIR, "..", "data", "knowledge_base.txt")
golden_dataset_path = os.path.join(BASE_DIR, "..", "eval", "golden_dataset.json")

def main():
    print("🔍 Running LLM Evaluation on Golden Dataset...")

    with open(knowledge_path, "r", encoding="utf-8") as f:
        knowledge = f.read()

    print(f"- Loading knowledge base from: {knowledge_path}")

    conversation_manager = ConversationManager()
    evaluator = Evaluator(conversation_manager)

    evaluator.evaluate(golden_dataset_path, knowledge)

if __name__ == "__main__":
    main()