############## FOR DOCKER DEPLOYMENT DOCKER FILE ###############################

<!-- for docker deployment -->

- FROM python:3.9-slim
- COPY . /app
- WORKDIR /app
- COPY requirements.txt .
- RUN pip install  -r requirements.txt
- EXPOSE $PORT
### for Docker Creation And Deployment
- CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] # this is for deployment
- CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app #for heroku cloud docker deployment



########### GITHUB ACTIONS FOR CI CD PIPELINE #########################################################
- For Configuration of github action two folders is needed .github and workflows
- .github/workflows and .github/workflows/main.yaml


