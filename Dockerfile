FROM openfabric/tee-python-cpu:latest

RUN mkdir application
WORKDIR /application
COPY . .
RUN poetry install -vvv --no-dev
RUN pip install langchain
RUN pip install spacy
RUN pip install transformers
RUN pip install google-api-python-client
RUN pip install TensorFlow
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz --no-deps
RUN pip install --upgrade pydantic typing-extensions
EXPOSE 5500
CMD ["sh","start.sh"]