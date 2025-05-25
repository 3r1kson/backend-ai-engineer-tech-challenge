from fastapi import FastAPI

# from src.config.config import Base, engine
from src.app.api.routes import router as api_router

from src.app.models.message_model import MessageModel
from src.app.models.conversation_context_model import ConversationContext
from src.app.models.analysis_result_model import AnalysisResult
from src.app.models.actionable_output_model import ActionableOutput
from src.app.models.process_message_response import ProcessMessageResponse
from src.app.models.process_message_request import ProcessMessageRequest

# Base.metadata.create_all(bind=engine)

def create_app():
    app = FastAPI(title="Tech Challenge API")
    app.include_router(api_router, prefix="/api")
    return app

app = create_app()