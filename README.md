![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)

<!-- LOGO -->
<br />
<h1>
<p align="center">
  <img src="https://raw.githubusercontent.com/ApexAgante/ApexAgenteSimple/main/img/new_logo.png" alt="Logo" width="140" height="140">
  <br>ApexAgente
</h1>
  <p align="center">
    Python application to check Apex agent in Trend Micro.
    <br />
    </p>
</p>
<p align="center">
  <a href="#about-the-project">About The Project</a> •
  <a href="#importing">Importing</a> •
  <a href="#installation">Installation</a> • 
  <a href = "#dependencies-installation">Dependencies Installation</a> •
  <a href="#run-locally">Run Locally</a>
</p>

## About The Project

Apex Agente is a powerful Python application designed to gather data from Trend Micro Apex URL, a cloud-based security platform that provides advanced threat protection for enterprise networks. With Apex Agente, you can easily retrieve all available data from the Apex URL or retrieve specific data by hostname.

The first feature of Apex Agente allows you to retrieve all data from the Apex URL, giving you a comprehensive view of all datas available. This data can include information on host name, entity id, registration ip, and last registration time.

The second feature of Apex Agente allows you to retrieve data specific to a particular host name. This feature is particularly useful if you want to drill down into getting deeper information of a particular host or agent. With this feature, you can retrieve information on a host which included name, entity id, server id, registration ip, connection status, etc.

Apex Agente is easy to use and comes with a simple and intuitive user interface. It is designed to work with Trend Micro Apex URL, so you can be confident that the data you retrieve is accurate and up-to-date. Whether you are a security professional, network administrator, or IT manager, Apex Agente is a must-have tool for monitoring the security status of your network and ensuring that your organization stays safe from potential threats.

## Importing

To have the application, you need to import from github

- CLI
    ```bash
    git clone -b cli https://github.com/ApexAgante/ApexAgente
    ```
- GUI
    ```bash
    git clone -b gui https://github.com/ApexAgante/ApexAgente
    ```

## Installation

### Directory
Go to the cloned project by using:
```bash
cd ApexAgente
```

### Environment <small>optional</small>
We recommend using a virtual environment, which is an isolated Python runtime. If you are in a virtual environment, any package that you install or upgrade will be local to the environment.
If you run into problem, you can just delete and recreate the environment. It's trivial to set up:

<details> 

<summary>poetry <small><strong>strongly recommend</strong></small></summary>

- Poetry automaticcaly created virtual environment
- Activate the environment with:
    ```bash
    poetry shell
    ```
- Exit your virtual environment using:
    ```bash
    exit
    ```

</details>

<details>

<summary>pipenv <small>recommend</small></summary>

- Pipenv automatically created virtual environment
- Activate the environment with
    ```bash
    pipenv shell
    ```
- Exit your virtual environment using:
    ```bash
    exit
    ```

</details>

<details>

<summary>pip</summary>

- Create a new virtual environment
    ```bash
    python -m venv venv
    ```
- Activate the environment with:
    ```bash
    . venv/bin/activate (Linux / MacOS) / . venv/Scripts/activate (Windows)
    ```
- Exit your virtual environment using:
    ```bash
    deactivate
    ```

</details>

## Dependencies Installation
Apex Agente has several dependencies that can be installed with `poetry`, `pipenv` or `pip`, ideally by using a virtual environment. Open up a terminal and install all dependencies with:

- poetry
    ```bash
    poetry install
    ```
- pipenv
    ```bash
    pipenv sync
    ```
- pip
    ```bash
    pip install -r requirements.txt
    ```

This will automatically install compatible versions of all dependencies. ApexAgente always strive to support the latest versions, so there's no need to install packages separately.

## Run Locally
To run it locally is pretty simple, just run it with:

- poetry
    ```bash
    poetry run app [--api API KEY] [--id APPLICATION ID] [--url SERVER URL] [--n DEFAULT CONFIGURATION]
    ```

- pipenv
    ```bash
    poetry run app [--api API KEY] [--id APPLICATION ID] [--url SERVER URL] [--n DEFAULT CONFIGURATION]
    ```

- python
    ```bash
    python -m app.main [--api API KEY] [--id APPLICATION ID] [--url SERVER URL] [--n DEFAULT CONFIGURATION]
    ```

> **Information**
>
> - The `--api` option specifies api key used in the application.
> - The `--id` option specifies application id used in the application
> - The `--url` option serves as base url for the application.
> - The `--n` option determine whether using the options or use default configuration. If you use `--n` you do not need to use other options.
>
> *Note: The program can be run without the need for the user to specify any options.*

## Usage Example
![Usage](./assets/usage.svg)
