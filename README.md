# api_serverless
Template for deployment of serverless application (Lambda + API Gateway) with Python 3.7

#### **Getting Started**
Create a python Flask Project as a global package

`pip install flask flask_cors`

Install cx_Oracle for Windows as a global package

`pip install cx_Oracle`

Download Instant Client for Windows (x64 / x32)
https://www.oracle.com/mx/database/technologies/instant-client/winx64-64-downloads.html

Unzip the file instantclient-basic-windows.x64-19.3.0.0.0dbru.zip into your root directory

Add the path of the instantclient_19_3 directory to the environment variables

Install boto3 as a global package 

`pip install boto3`

Install pymongo as a local package

`pip install pymongo -t .`

Create a **serverless.yml** file in the root directory of the project

#### **Prerequisites**

Install serverless framework in the root directory of the project

`npm install -g serverless`

Setup AWS credentials into serverless framework

`serverless config credentials --provider aws --key YOUR_KEY_ID --secret YOUR_SECRET_KEY_ID --profile PROFILE`

Install serverless plugins

`sls plugin install -n serverless-wsgi`

`sls plugin install -n serverless-python-requirements`

`npm install serverless-deployment-bucket`

`npm install serverless-domain-manager --save-dev`

#### **Run and test**

**Local deployment**

`sls wsgi serve`

**Deploy into AWS**

Deploy to admin serverless API
`sls deploy  --aws-profile YOUR_PROFILE --stage admin`

Deploy to app serverless API
`sls deploy  --aws-profile YOUR_PROFILE --stage app`
