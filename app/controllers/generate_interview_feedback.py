from flask import jsonify
from langchain.prompts import PromptTemplate
from utils.vertexAIclient import get_vertex_client

# refer components / mockinterview / interview.tsx file 
# inside endInterval Function call is made for this according to that fucntion return the response after proccesing here 

def generate_interview_feedback():
    # test code to check vertex ai , refernce to use vertex ai 
    try:
        # Get the Vertex AI client from the app context
        vertex_client = get_vertex_client()
        
        # Define a simple LangChain PromptTemplate
        prompt_template = PromptTemplate(
            input_variables=["task"],
            template="Please perform the following task: {task}",
        )
        
        # Define a small test task
        task = "Write a motivational quote"

        # Build the final prompt
        prompt = prompt_template.format(task=task)

        # Send the prompt to Vertex AI
        response_text = vertex_client.send_prompt(prompt)

        # Return the response as JSON
        return jsonify({'response': response_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    