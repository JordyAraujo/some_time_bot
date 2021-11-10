FROM python:3.6
USER root
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN apt-get update && apt-get -y install locales
RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG pt_BR.UTF-8  
ENV LANGUAGE pt_BR:pt  
ENV LC_ALL pt_BR.UTF-8
ENV MODE dev
RUN pip install -r requirements.txt