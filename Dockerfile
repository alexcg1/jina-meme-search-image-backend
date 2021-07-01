FROM jinaai/jina:2.0.0-py38

ARG docs_to_index=10

COPY . /workspace
WORKDIR /workspace

RUN apt-get update 
RUN apt-get -y install wget curl 
RUN pip install --no-cache-dir --retries=10 --timeout=1000 -r requirements.txt 
RUN sh get_data.sh 
RUN python get_images.py $docs_to_index 
RUN sh get_model.sh 
RUN python app.py -t index -n $docs_to_index 
RUN rm -rf data

ENTRYPOINT ["python", "app.py" , "-t", "query_restful"]
