FROM jinaai/jina:2.0.0-py38

#ARG docs_to_index=10

COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get -y install wget curl && pip install --no-cache-dir --retries=10 --timeout=1000 -r requirements.txt && sh get_data.sh && python get_images.py $docs_to_index && sh get_model.sh 
#RUN python app.py -t index -n $docs_to_index && rm -rf data

ENTRYPOINT ["python", "app.py" , "-t", "query_restful"]
