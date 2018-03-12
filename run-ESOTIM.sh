sudo docker build --network=host -t test-docker .
sudo docker run --network=host -v ${PWD}/Doublons/:/usr/src/app/target  test-docker
sudo chown $USER ${PWD}/Doublons/ -Rf