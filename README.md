# Handwritten or Printed Image Classifier (MHWC) RestAPI

An API to classify an Image as handwritten or printed

## Solution Flow Diagram

![MHWC Model Diagram](imgs/dummy-flow.jpg)

## Implementation

### Development Setup

Setup the conda environment and load the necessary requirements.

```python
conda create --name=MHWC python=3.8
# accept all inputs
# Install requirements [Development]
pip install -r requirements-dev.txt
pip install -r requirements.txt

# Install requirements [Prd]
pip install -r requirements.txt
```

### Service Setup

Export environment variables

```shell
export APP_ACRONYM=MHWC
export MODE=development
export CFG_KEY='?'
export CFG_SECRET="?"
```

```python
uvicorn app.MHWC_app:app --port 8353 --host 0.0.0.0
```

Open browser on url:

- http://server_ip:8123/docs

Code changes made will be auto loaded for action.

[VERSIONS]

### v1.0.0 -> 30th Jan 2023
