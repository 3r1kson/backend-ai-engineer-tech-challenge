# Backend - AI Engineer technical challenge

---

## System instructions

## Migration
````
example:

    alembic revision --autogenerate -m "commit information"
    alembic upgrade head
````

---

## System Information

## Folder Structure

    |-- .venv
    |-- src
    |   |-- app
    |   |   |-- api
    |   |   |   |-- routes.py
    |   |   |-- data
    |   |   |   |-- knowledge_base.txt
    |   |   |-- eval
    |   |   |   |-- evaluator.py
    |   |   |   |-- golden_dataset.json
    |   |   |-- llm
    |   |   |   |-- llm_handler.py
    |   |   |-- models
    |   |   |   |-- actionable_output_model.py
    |   |   |   |-- analysis_result_model.py
    |   |   |   |-- conversation_context_model.py
    |   |   |   |-- message_model.py
    |   |   |   |-- process_message_request.py
    |   |   |   |-- process_message_response.py
    |   |   |-- services
    |   |   |   |-- conversation_manager_service.py
    |   |   |   |-- message_service.py
    |   |   |-- tests
    |   |   |   |-- app
    |   |   |   |   |-- test_message_service.py
    |   |   |-- tools
    |   |   |   |-- crm_tool.py
    |   |   |   |-- rag_tool.py
    |   |   |   |-- run_evaluation.py
    |   |   |-- assets
    |   |   |   |-- images
    |   |   |   |   |-- DBStructure_backendAIEngeneerTechChallenge_Erikson.png
    |   |-- config
    |   |   |-- config.py
    |   |-- instance (provisory)
    |   |   |-- tech_challenge.db
    |   |-- main.py
    |   |-- run.py
    |-- pytest.ini
    |-- README.md
    |-- requirements.txt

## Database Structure (Not implemented)

    // AI Sales Agent Contextual Database
    // DBML version
    
    Table conversation_context {
      id integer [primary key]
      topic varchar(255)
      created_at timestamp
    }
    
    Table message {
      id integer [primary key]
      sender varchar(20)
      content text
      timestamp timestamp
      conversation_id integer [not null]
    }
    
    Table analysis_results {
      id integer [primary key]
      key_points text
      sentiment varchar(50)
      action_required varchar(100)
      conversation_id integer [not null]
    }
    
    Table actionable_outputs {
      id integer [primary key]
      response_text text [not null]
      action_type varchar(100)
      created_at timestamp
      analysis_result_id integer [not null]
    }
    
    // Relationships
    Ref: message.conversation_id > conversation_context.id
    Ref: analysis_results.conversation_id > conversation_context.id
    Ref: actionable_outputs.analysis_result_id > analysis_results.id

### Visual context of database structure
![Database Diagram](src/assets/images/DBStructure_backendAIEngeneerTechChallenge_Erikson.png)
