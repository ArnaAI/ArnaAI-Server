import os
import json
from flask import current_app, request, jsonify
from werkzeug.utils import secure_filename
from google.oauth2 import service_account
from langchain_google_vertexai import VertexAI
import fitz  # PyMuPDF for PDF parsing

class VertexAIClient:
    def __init__(self, model_name: str, credentials):
        """Initialize Vertex AI client using LangChain Google VertexAI."""
        self.model_name = model_name
        self.llm = VertexAI(model_name=self.model_name, credentials=credentials)

    def send_prompt(self, prompt: str) -> str:
        """Send a prompt to the Vertex AI model and return the response."""
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            raise RuntimeError(f"Error communicating with Vertex AI: {str(e)}")

def init_vertex_ai(app, model_name: str, credentials):
    """Initialize the Vertex AI client and store it in the Flask app context."""
    try:
        app.config['VERTEX_CLIENT'] = VertexAIClient(model_name, credentials)
        print("Vertex AI client initialized and stored in app context.")
    except Exception as e:
        print(f"Error during Vertex AI client initialization: {str(e)}")
        raise e

def get_vertex_client():
    """Retrieve the Vertex AI client from the Flask app context."""
    client = current_app.config.get('VERTEX_CLIENT')
    if not client:
        raise RuntimeError("Vertex AI client is not initialized in app context.")
    return client

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        with fitz.open(pdf_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {str(e)}")

def process_resume_and_analyze():
    """Process an uploaded resume, extract text, and analyze with Vertex AI."""
    try:
        # Check if a file is included in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request."}), 400

        file = request.files['file']

        # Ensure a file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected."}), 400

        # Save the uploaded file securely
        filename = secure_filename(file.filename)
        upload_path = os.path.join("./uploads", filename)
        file.save(upload_path)

        # Extract text from the PDF file
        extracted_text = extract_text_from_pdf(upload_path)

        # Get the Vertex AI client
        vertex_client = get_vertex_client()

        # Construct the prompt for analysis
        prompt = (
            """
Analyze this resume and provide a detailed and comprehensive analysis in the following format:
**ATS Score**  
[Provide a score out of 100 based on criteria such as keyword optimization, formatting, section arrangement, and relevance of content for Applicant Tracking Systems.]
**Strengths**  
* List all strengths in alignment with the resume sections. Use a single bullet for each strength, starting with the section name followed by details. For example:  
  - **Skills:** Strong expertise in JavaScript, React.js, and Node.js, aligned with industry requirements.  
  - **Education:** High academic performance with a CGPA of 9.10, showcasing a solid academic foundation.  
**Weaknesses**  
* Highlight weaknesses section-wise, identifying specific areas of improvement. Use a single bullet per weakness, starting with the section name followed by details. For example:  
  - **Work Experience:** Lacks quantifiable achievements, making it harder to gauge impact.  
  - **Skills:** Missing important certifications relevant to the role, such as AWS or DevOps.  
**Suggestions**  
* Provide actionable recommendations to enhance each section, ensuring the resume becomes more impactful and ATS-friendly. Use a single bullet per suggestion, starting with the section name followed by details. For example:  
  - **Work Experience:** Include measurable results, such as "Increased user engagement by 20% through optimization."  
  - **Skills:** Add certifications in trending technologies like AWS or DevOps to strengthen technical credibility.  
Ensure the analysis is detailed, section-specific, and offers constructive feedback. Focus on improving the overall appeal for both ATS and recruiters.
"""

        )

        # Analyze the text using Vertex AI
        analysis_result = vertex_client.send_prompt(prompt)

        # Return the analysis as a JSON response
        return jsonify({"analysis": analysis_result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def start_vertex(app):
    """Initialize the Vertex AI client and configure the environment."""
    service_account_path = "./gcp_cred.json"

    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path

    # Load credentials from the service account key file
    credentials = service_account.Credentials.from_service_account_file(service_account_path)

    with open(service_account_path, 'r') as file:
        credentials_data = json.load(file)

    # Print the details (e.g., project_id and client_email)
    print("Project ID:", credentials_data.get('project_id'))
    print("Client Email:", credentials_data.get('client_email'))

    # Initialize the Vertex AI client and store it in the app context
    init_vertex_ai(app, "gemini-pro", credentials)

#new one 
# import os
# import json
# from flask import current_app, request, jsonify
# from werkzeug.utils import secure_filename
# from google.oauth2 import service_account
# from langchain_google_vertexai import VertexAI
# import fitz  # PyMuPDF for PDF parsing
# from langchain.prompts import PromptTemplate
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains import SequentialChain, LLMChain
# from langchain.memory import ConversationBufferMemory

# # VertexAIClient Class
# class VertexAIClient:
#     def __init__(self, model_name: str, credentials):
#         """Initialize Vertex AI client using LangChain Google VertexAI."""
#         self.model_name = model_name
#         self.llm = VertexAI(model_name=self.model_name, credentials=credentials)

#     def send_prompt(self, prompt: str) -> str:
#         """Send a prompt to the Vertex AI model and return the response."""
#         try:
#             response = self.llm.invoke(prompt)
#             return response
#         except Exception as e:
#             raise RuntimeError(f"Error communicating with Vertex AI: {str(e)}")

# # Initialize Vertex AI Client
# def init_vertex_ai(app, model_name: str, credentials):
#     """Initialize the Vertex AI client and store it in the Flask app context."""
#     try:
#         app.config['VERTEX_CLIENT'] = VertexAIClient(model_name, credentials)
#         print("Vertex AI client initialized and stored in app context.")
#     except Exception as e:
#         print(f"Error during Vertex AI client initialization: {str(e)}")
#         raise e

# # Retrieve Vertex Client
# def get_vertex_client():
#     """Retrieve the Vertex AI client from the Flask app context."""
#     client = current_app.config.get('VERTEX_CLIENT')
#     if not client:
#         raise RuntimeError("Vertex AI client is not initialized in app context.")
#     return client

# # Extract Text from PDF
# def extract_text_from_pdf(pdf_path):
#     """Extracts text from a PDF file."""
#     try:
#         with fitz.open(pdf_path) as pdf:
#             text = ""
#             for page in pdf:
#                 text += page.get_text()
#         return text
#     except Exception as e:
#         raise RuntimeError(f"Error extracting text from PDF: {str(e)}")

# # Prompt Generation
# def get_analysis_prompt(resume_text):
#     """Generate a structured prompt using LangChain PromptTemplate."""
#     prompt_template = PromptTemplate(
#         input_variables=["resume_text"],
#         template=(
#             "Analyze this resume and provide a detailed analysis in the following format:\n"
#             "**ATS Score**\n"
#             "[Provide a score out of 100 based on criteria such as keyword optimization, formatting, section arrangement, and relevance.]\n"
#             "**Strengths**\n"
#             "* List all strengths.\n"
#             "**Weaknesses**\n"
#             "* Highlight weaknesses.\n"
#             "**Suggestions**\n"
#             "* Provide actionable recommendations.\n\n"
#             "Resume text:\n{resume_text}"
#         )
#     )
#     return prompt_template.format(resume_text=resume_text)

# # Text Splitting
# def split_resume_text(resume_text):
#     """Split resume text into manageable chunks."""
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=100
#     )
#     return splitter.split_text(resume_text)

# # Create Analysis Chain
# def create_analysis_chain(llm):
#     """Create a sequential chain for summarization and analysis."""
#     summarize_prompt = PromptTemplate(
#         input_variables=["text"],
#         template="Summarize the following resume text:\n{text}"
#     )
#     summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

#     analyze_prompt = PromptTemplate(
#         input_variables=["summary"],
#         template="Analyze this summarized resume:\n{summary}"
#     )
#     analyze_chain = LLMChain(llm=llm, prompt=analyze_prompt)

#     chain = SequentialChain(
#         chains=[summarize_chain, analyze_chain],
#         input_variables=["text"],
#         output_variables=["analysis"]
#     )
#     return chain

# # Process Resume and Analyze
# def process_resume_and_analyze():
#     """Process an uploaded resume, extract text, and analyze with Vertex AI."""
#     try:
#         if 'file' not in request.files:
#             return jsonify({"error": "No file part in the request."}), 400

#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No file selected."}), 400

#         filename = secure_filename(file.filename)
#         upload_path = os.path.join("./uploads", filename)
#         file.save(upload_path)

#         extracted_text = extract_text_from_pdf(upload_path)

#         chunks = split_resume_text(extracted_text)
#         analysis_results = []

#         vertex_client = get_vertex_client()
#         for chunk in chunks:
#             prompt = get_analysis_prompt(chunk)
#             analysis_results.append(vertex_client.send_prompt(prompt))

#         analysis_combined = "\n\n".join(analysis_results)
#         return jsonify({"analysis": analysis_combined}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Start Vertex AI
# def start_vertex(app):
#     """Initialize the Vertex AI client and configure the environment."""
#     service_account_path = "./gcp_cred.json"
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path

#     credentials = service_account.Credentials.from_service_account_file(service_account_path)

#     with open(service_account_path, 'r') as file:
#         credentials_data = json.load(file)

#     print("Project ID:", credentials_data.get('project_id'))
#     print("Client Email:", credentials_data.get('client_email'))

#     init_vertex_ai(app, "gemini-pro", credentials)
