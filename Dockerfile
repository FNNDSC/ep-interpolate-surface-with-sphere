FROM docker.io/fnndsc/mni-conda-base:civet2.1.1-python3.10.2

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="ep-interpolate-surface-with-sphere" \
      org.opencontainers.image.description="Resample surface meshes to have 81,920 triangles."

WORKDIR /usr/local/src/ep-interpolate-surface-with-sphere

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["isws", "--help"]
