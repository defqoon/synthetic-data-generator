FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update && \
    apt-get install -y \
        bzip2 \
        git \
        libfontconfig1 \
        libgconf-2-4 \
        libglu1 \
        libsm6 \
        libxext6 \
        libxrender1 \
        unrar \
        vim \
        wget

WORKDIR /root/
RUN wget -c --quiet download.blender.org/release/Blender2.79/blender-2.79a-linux-glibc219-x86_64.tar.bz2 && \
    tar -xf blender-2.79a-linux-glibc219-x86_64.tar.bz2 && \
    rm blender-2.79a-linux-glibc219-x86_64.tar.bz2 && \
    mv blender-2.79a-linux-glibc219-x86_64/ blender/ && \
    cp -r blender /usr/lib/blender && \
    echo "export PATH="/usr/lib/blender:$PATH"" >> /root/.bashrc


COPY /src/requirements.txt /root/
COPY src /root/aquabyte_cv_datagen
RUN pip install -r /root/requirements.txt

RUN pip install --user git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI