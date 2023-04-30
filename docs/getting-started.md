---
template: main.html
title: Getting started
---

# Getting started
![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)

## About The Project

Apex Agente is a powerful Python application designed to gather data from Trend Micro Apex URL, a cloud-based security platform that provides advanced threat protection for enterprise networks. With Apex Agente, you can easily retrieve all available data from the Apex URL or retrieve specific data by hostname.

The first feature of Apex Agente allows you to retrieve all data from the Apex URL, giving you a comprehensive view of all datas available. This data can include information on host name, entity id, registration ip, and last registration time.

The second feature of Apex Agente allows you to retrieve data specific to a particular host name. This feature is particularly useful if you want to drill down into getting deeper information of a particular host or agent. With this feature, you can retrieve information on a host which included name, entity id, server id, registration ip, connection status, etc.

Apex Agente is easy to use and comes with a simple and intuitive user interface. It is designed to work with Trend Micro Apex URL, so you can be confident that the data you retrieve is accurate and up-to-date. Whether you are a security professional, network administrator, or IT manager, Apex Agente is a must-have tool for monitoring the security status of your network and ensuring that your organization stays safe from potential threats.

## Importing

=== "CLI"

    ```sh
        git clone -b cli https://github.com/ApexAgante/ApexAgente
    ```

=== "GUI"

    ```sh
        git clone -b gui https://github.com/ApexAgante/ApexAgente
    ```

## Installation

### Directory
Go to your project directory by using:
``` bash
cd ApexAgente
```


### Dependencies Installation
Apex Agente has several dependencies that can be installed with
`poetry` or `pip`, ideally by using a [virtual environment](https://docs.python.org/3/library/venv.html). Open up a terminal and install all dependencies with:

#### with poetry <small>recommended</small> { #with-poetry data-toc-label="with poetry" }
=== "Latest"
    ```sh
    poetry install # (1)!
    ```

    1. This will install dependencies with poetry

#### with pip
=== "Latest"
    ```sh
    pip install -r requirements.txt # (1)!
    ```

    1. This will install dependencies with python pip

This will automatically install compatible versions of all dependencies. ApexAgente always strives to support the latest versions, so there's no need to install those packages separately.

## Run Locally

To run it locally is pretty simple, just run it with:
=== "Poetry"
    
    ``` bash
    poetry run app
    ```

=== "Python"

    ``` bash
    python3 -m app/main.py
    ```
