FROM python:3.6

RUN apt-get update && \
    apt-get install -y \
        bzip2 \
        git \
        git-core \
        libfontconfig1 \
        libgconf-2-4 \
        libglu1 \
        libsm6 \
        libxext6 \
        libxrender1 \
        vim \
        wget

WORKDIR /root/
RUN wget -c --quiet download.blender.org/release/Blender2.79/blender-2.79a-linux-glibc219-x86_64.tar.bz2 && \
    tar -xf blender-2.79a-linux-glibc219-x86_64.tar.bz2 && \
    rm blender-2.79a-linux-glibc219-x86_64.tar.bz2 && \
    mv blender-2.79a-linux-glibc219-x86_64/ blender/ && \
    cp -r blender /usr/lib/blender && \
    echo "export PATH="/usr/lib/blender:$PATH"" >> /root/.bashrc


COPY /src/requirements.txt /root
RUN pip3 install -r /root/requirements.txt

RUN pip3 install --user git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI

COPY models /root/models/
COPY src /root/
COPY deploy/config.json /root/

CMD ["python3", "dataset_creation.py"]
# ENTRYPOINT ["/root/entrypoint.sh"]
#EXPOSE 8889
#CMD ["jupyter notebook", "--ip=0.0.0.0", "--allow-root", "--port=8889"]
