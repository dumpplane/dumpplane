FROM python:3.9

COPY dist/dumpplane-0.0.2-py3-none-any.whl /dumpplane-0.0.2-py3-none-any.whl

RUN pip install /dumpplane-0.0.2-py3-none-any.whl

RUN pip install pyyaml
RUN pip install elasticsearch
RUN pip install pymongo
RUN pip install kubernetes
