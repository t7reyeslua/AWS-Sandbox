## Installation Steps

These instructions were tested in an Ubuntu 16.04 installation for Python 3.5.2

1. Follow the steps in [Amazon Rekogntion: Getting Started](http://docs.aws.amazon.com/rekognition/latest/dg/getting-started.html) which basically are:
  * [Set Up an AWS Account and Create an Administrator User](http://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html)
  * [Set Up the AWS Command Line Interface](http://docs.aws.amazon.com/rekognition/latest/dg/setup-awscli.html) for configuring the credentials to be used. The code could also receive the credentials programatically, but currently it shows an error. However, if the credentials are properly configured for using the awscli that is enough.
2. Install AWS Python SDK:
   ```
   pip3 install boto3
   ```
3. Install Python3 PIL Pillow for image processing. Used for cropping images.
   ```
   sudo apt-get install python3-pil
   ```
4. [Install OpenCV for Python3](http://cyaninfinite.com/tutorials/installing-opencv-in-ubuntu-for-python-3/). Used for video capturing. Needs to be built. [Also used this guide](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
  * Download dependencies:
    ```
    sudo apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran python3-numpy python3-matplotlib
    ```
  * Download developer packages for Python 3:
    ```
    sudo apt-get install python3.5-dev
    ```
  * Download source coude:
  ```
      cd ~/Downloads
      mkdir OpenCV
      cd OpenCV
      wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
      wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
      unzip opencv.zip
      unzip opencv_contrib.zip
  ```
  * Build:
  ```
      cd opencv-3.1.0/
      mkdir build
      cd build
      cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D INSTALL_C_EXAMPLES=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=~/Downloads/OpenCV/opencv_contrib-3.1.0/modules \
      -D BUILD_EXAMPLES=ON ..
  ```
  * Make and install:
  ```
      make
      sudo make install
      sudo ldconfig
  ```
5. Install watchdog for polling for new screenshot taken:
   ```
      pip3 install watchdog
   ```
6. Install MQTT dependencies:
  * Add MQTT serve repository and install
  ```
      sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
      sudo apt-get update
      sudo apt-get install mosquitto mosquitto-clients
   ```
  * Install MQTT python package
   ```
      pip3 install paho-mqtt
   ```
