__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import os
import shutil
import click
import sys
from glob import glob
import base64
import pretty_errors

from jina import Flow, DocumentArray, Document

# from jina.types.document.generators import from_files
# from jina.logging import logger
from config import (
    max_docs,
    images_dir,
    backend_workdir,
    backend_port,
    random_seed,
    backend_datafile,
)


def prep_docs(input_file, max_docs=max_docs, shuffle=True, images_dir=images_dir):
    print(f"Preparing {max_docs} Documents")
    import json

    memes = []
    print(f"Processing {input_file}")
    with open(input_file, "r") as file:
        raw_json = json.loads(file.read())

    for template in raw_json:
        for meme in template["generated_memes"]:
            meme["template"] = template["name"]
        memes.extend(template["generated_memes"])

    if shuffle:
        import random

        random.seed(random_seed)
        random.shuffle(memes)

    os.chdir(images_dir)
    for meme in memes[:max_docs]:

        # Download image
        import requests

        url = f'http:{meme["image_url"]}'
        filename = meme["image_url"].split("/")[-1]
        try:
            r = requests.get(url, allow_redirects=True)
            if r.status_code == 200:
                with open(filename, "wb") as file:
                    file.write(r.content)
                # Set Document content to downloaded image
                fixed_path = images_dir.split(".")[-1]
                path_to_image = f"./{fixed_path}/{filename}"
                doc = Document(uri=path_to_image)
                # Set Document tags to metadata
                doc.tags = meme
                print(doc)

                yield doc
        except:
            print(f"Error on {filename}, skipping.")


os.environ["JINA_WORKSPACE"] = backend_workdir
os.environ["JINA_PORT"] = str(backend_port)

# types = (f"{images_dir}/*.png", f"{images_dir}/*.jpg")
# files_grabbed = []
# for files in types:
# files_grabbed.extend(glob(files))


# def build_file_list(images_dir):
# types = (f"{images_dir}/*.png", f"{images_dir}/*.jpg")
# files_grabbed = []
# for files in types:
# files_grabbed.extend(glob(files))

# return files_grabbed


def encode_image_to_base64(image_file):
    with open(image_file, "rb") as file:
        encoded_image = base64.b64encode(file.read())
        encoded_image = str(encoded_image)

    return encoded_image


# def create_docarray(file_list):
# """
# Create DocArray
# Each doc.content = file
# Each doc["tags"]["raw_image"] = file (base64 encoded)
# That way the content will be munged by Jina but original file will exist in tags. So searching is efficient but can return full-res memes
# """
# docs = DocumentArray()
# docs = []
# for image_file in file_list:
# doc = Document(uri=image_file)
# doc.tags = {"base64_image": encode_image_to_base64(image_file)}
# print(doc)

# docs.append(doc)

# return docs


def index(input_docs, num_docs: int = max_docs):
    # Runs indexing for all images

    with Flow.load_config("flows/index.yml") as flow:
        flow.post(
            on="/index",
            inputs=input_docs,
            request_size=64,
            read_mode="rb",
        )


def query_restful():
    # Starts the restful query API
    flow = Flow.load_config("flows/query.yml")
    flow.use_rest_gateway()
    with flow:
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "query_restful"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=max_docs)
@click.option("--force", "-f", is_flag=True)
def main(task: str, num_docs: int, force: bool):
    workspace = os.environ["JINA_WORKSPACE"]
    if task == "index":
        # image_files = build_file_list(images_dir)
        # docs = create_docarray(image_files)
        if os.path.exists(workspace):
            if force:
                shutil.rmtree(workspace)
            else:
                print(
                    f"\n +----------------------------------------------------------------------------------+ \
                        \n |                                   🤖🤖🤖                                         | \
                        \n | The directory {workspace} already exists. Please remove it before indexing again.  | \
                        \n |                                   🤖🤖🤖                                         | \
                        \n +----------------------------------------------------------------------------------+"
                )
                sys.exit(1)
        docs = prep_docs(input_file=backend_datafile, max_docs=num_docs)
        index(docs, num_docs)
    if task == "query_restful":
        if not os.path.exists(workspace):
            print(
                f"The directory {workspace} does not exist. Please index first via `python app.py -t index`"
            )
            sys.exit(1)
        query_restful()


if __name__ == "__main__":
    main()
