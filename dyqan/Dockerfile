FROM python:3.8

# Настроить и активировать виртуальную среду
ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

# Команды Python будут выполнены в виртуальной среде
COPY . /dyqan
RUN pip install --no-cache-dir -r /dyqan/requirements.txt
WORKDIR /dyqan
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

EXPOSE 8000