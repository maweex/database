FROM python
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
EXPOSE 5000
COPY . .
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]