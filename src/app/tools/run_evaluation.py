# app
from src.app.services.conversation_manager_service import ConversationManager
from src.app.eval.evaluator import Evaluator

def main():
    print("🔍 Running LLM Evaluation on Golden Dataset...")

    conversation_manager = ConversationManager()
    evaluator = Evaluator(conversation_manager)

    evaluator.evaluate("/home/erik/PycharmProjects/[Backend-AI_Engineer]Technical_Challenge_Erikson/src/app/eval/golden_dataset.json")

if __name__ == "__main__":
    main()
