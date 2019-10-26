FROM python:3.6.8
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /src
RUN mkdir /static
WORKDIR /src
ADD ./ /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python manage.py collectstatic
CMD python manage.py migrate