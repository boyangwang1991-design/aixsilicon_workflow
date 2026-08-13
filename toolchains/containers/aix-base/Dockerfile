# AIXSILICON 开源基础镜像：Python + FuseSoC + Verilator
# 仅包含开源工具；商业 EDA 由受控 Runner/module 提供，不写入本镜像。
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        make \
        gcc \
        g++ \
        bison \
        flex \
        libfl2 \
        libfl-dev \
        libreadline-dev \
        libjson-c-dev \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Verilator (pinned major)
RUN git clone --depth 1 --branch v5.020 https://github.com/verilator/verilator.git /opt/verilator-src \
    && cd /opt/verilator-src \
    && autoconf && ./configure --prefix=/opt/verilator \
    && make -j"$(nproc)" && make install \
    && rm -rf /opt/verilator-src

ENV PATH="/opt/verilator/bin:${PATH}"

RUN pip install --no-cache-dir \
        fusesoc==2.4.* \
        "PyYAML>=6.0" \
        "jsonschema>=4.18"

WORKDIR /work
ENTRYPOINT ["/bin/bash"]
