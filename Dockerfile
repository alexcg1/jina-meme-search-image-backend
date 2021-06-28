FROM jinaai/jina:2.0.0rc4-py38

# setup the workspace
COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get install --no-install-recommends -y git curl libmagic1 wget tar \
    && pip uninstall -y jina && pip install -r requirements.txt

#RUN python get_data.py && bash get_model.sh && python app.py -t index

ENTRYPOINT ["python", "app.py", "-t", "query_restful"]

LABEL author="alex.cg@jina.ai"
LABEL type="app"
LABEL kind="example"
LABEL avatar="None"
LABEL description="Jina app to search memes by image"
LABEL documentation="https://github.com/alexcg1/jina-meme-search-image-backend"
LABEL keywords="[memes, cv, Google Big Transfer]"
LABEL license="apache-2.0"
LABEL name="jina-memes-image-search"
LABEL platform="linux/amd64"
LABEL update="None"
LABEL url="https://github.com/alexcg1/jina-meme-search-image-backend"
LABEL vendor="Jina AI Limited"
LABEL version="0.3"
