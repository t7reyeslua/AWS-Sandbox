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
