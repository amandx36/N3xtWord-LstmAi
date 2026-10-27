# selected base image 
from python:3.12-slim

# set up woring dir 
workdir /app

copy requirement.txt .

run pip install -r requirement.txt

# copy dependices file 
copy . . 

run python  downloadModelAndVoc.py


expose 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]