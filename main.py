import os
import warnings
from typing import Dict

from openfabric_pysdk.utility import SchemaUtil

from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText

from openfabric_pysdk.context import Ray, State
from openfabric_pysdk.loader import ConfigClass
import os
import langchain
import spacy
from transformers import pipeline
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

# Add Google Search LLM with your API key and search engine ID
os.environ["GOOGLE_CSE_ID"] = 'd3564aae05d5945d3'
os.environ["GOOGLE_API_KEY"] = "AIzaSyB_TKdTp2SYXybtwgLROez6zWAEcDWuDd0"
search = GoogleSearchAPIWrapper()

tool = Tool(
    name="Google Search",
    description="Answer",
    func=search.run,
)

# Load NLP tools
nlp = spacy.load("en_core_web_sm")  # For entity extraction
summarizer = pipeline("summarization")  # For text summarization

def answer_with_nlp(query):
    # Retrieve initial response from Google Search
    text = tool.run(query)

    # Extract key entities
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]

    # Summarize relevant parts
    summary = summarizer(text, max_length=100, min_length=30)[0]["summary_text"]


    return summary, entities # Return summary, extracted entities


############################################################
# Callback function called on update config
############################################################
def config(configuration: Dict[str, ConfigClass], state: State):
    # TODO Add code here
    pass


############################################################
# Callback function called on each execution pass
############################################################
def execute(request: SimpleText, ray: Ray, state: State) -> SimpleText:
    output = []
    for text in request.text:
        # TODO Add code here
        summary, entities= answer_with_nlp(text)
        output.append(summary)

    return SchemaUtil.create(SimpleText(), dict(text=output))
