FROM python:3.5.2

WORKDIR /usr/src/app

#COPY requirements.txt ./
#RUN pip3 install --no-cache-dir -r requirements.txt

#RUN apt-get update ; apt-get -y install gettext
#RUN apt-get -y install python3-pyqt5

COPY ./ESOTIM ./ESOTIM/
#RUN cd ./ESOTIM ; make


COPY ./Import ./source/
RUN mkdir ./target/

ENV folderpath "/usr/src/app/source/"
ENV csvpath "/usr/src/app/target/"

ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["sh", "-c", "python ./ESOTIM/run.py ${folderpath} ${csvpath}"]
#CMD cd ./ESOTIM ; make run

# ENTRYPOINT "python ./ESOTIM/run.py"