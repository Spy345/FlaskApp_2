import json
import os
import sys
from dotenv import load_dotenv
load_dotenv(); #Loading the .env file
from flask import Flask, request, jsonify
import boto3
from botocore.config import Config

#Creating the Flask App
app = Flask(__name__)

module_path = ".."
sys.path.append(os.path.abspath(module_path)) #Provide The Direct Access to the Built-in Functions

aws_access_id = os.getenv("AWS_ACCESS_KEY_ID");
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY");
target_region="us-west-2"
# aws_session_token = os.getenv("AWS_SESSION_TOKEN");

# print(aws_access_id, aws_secret_access_key)

retry_config = Config(
        region_name=target_region,
        retries={
            "max_attempts": 10,
            "mode": "standard",
        },
    )

#starting session 
session = boto3.Session(
    region_name=target_region
);

#Using the session Client
boto3_bedrock = session.client(
    service_name="bedrock",
    config=retry_config,
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    )

if boto3_bedrock :
    print("Boto3 Client created Successfully!");

@app.route('/chat', methods=['GET', 'POST'])
def chat():
   
        #Accessing the Recieved JSON Body To Access the Body parameters 
        # data = request.get_json();
        
        #Get the Propmt From the Parameter
        # prompt_data = request.args.get('prompt');
        
        # body_str = data.get('body');
        
        # body_data = json.loads(body_str);
        # max_tokens = body_data.get('max_tokens_to_sample');
        
        # print(body_data.get('max_tokens_to_sample'))
        prompt_data = """Human: Give me details on Solar Panal Market.Make Bulleted Point's.
        
        Assistant:
        """
        
        body = json.dumps({"prompt": prompt_data, "max_tokens_to_sample": 500})
        modelId = "anthropic.claude-v2"  # change this to use a different version from the model provider
        accept = "application/json"
        contentType = "application/json"
        
        response = boto3_bedrock.invoke_model(
                body=body, modelId=modelId, accept=accept, contentType = contentType
                );

        response_body = json.loads(response.get("body").read());

        return jsonify( {'Response': response_body.get("completion")});      
           
if __name__ == '__main__':
    app.run(debug=True)



# List the Available AI model in AWS BedRock

# models = boto3_bedrock.list_foundation_models();
# print(models)



