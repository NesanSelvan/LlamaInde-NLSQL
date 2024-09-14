from sqlalchemy import (
    create_engine,
    MetaData,)

from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import Settings
import os
from llama_index.llms.gemini import Gemini
from prompts import sql_prompt
from llama_index.embeddings.gemini import GeminiEmbedding
from prompts import sql_prompt,synthesize_prompt
from llama_index.core import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_KEY')
SQL_POSTGRES = os.getenv('SQL_POSTGRES')

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

model_name = "models/embedding-001"

embed_model = GeminiEmbedding(
    model_name=model_name, api_key=GEMINI_API_KEY,
)
Settings.embed_model = embed_model

engine = create_engine(SQL_POSTGRES)
metadata_obj = MetaData()
sql_database = SQLDatabase(engine, include_tables=['movies'])

llm = Gemini(api_key=GEMINI_API_KEY)

Settings.llm = llm
query_engine = NLSQLTableQueryEngine(
    
    sql_prompt=PromptTemplate(sql_prompt),
    response_synthesis_prompt=PromptTemplate(synthesize_prompt),
    sql_database=sql_database, tables=["movies"], llm=llm,synthesize_response=True,verbose=True
)
query = "Compare Marvel and Dc ,Total Collection of both  and without using rating Give Conclusion from both who is better?"
response = query_engine.query(query)
print(response)
