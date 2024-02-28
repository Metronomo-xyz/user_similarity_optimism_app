FROM python:3.11.8-bookworm

WORKDIR /user_similarity_optimism_app

COPY . .

RUN pip install -r requirements.txt

workdir ../

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--chdir", "user_similarity_optimism_app", "app:app", "--timeout 30"]