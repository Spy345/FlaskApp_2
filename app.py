import json
import os
import sys
from dotenv import load_dotenv
load_dotenv(); #Loading the .env file
from flask import Flask, request, jsonify
import boto3
from botocore.config import Config

#Creating the Flask Instance
app = Flask(__name__)

module_path = ".."
sys.path.append(os.path.abspath(module_path)) #Provide The Direct Access to the Built-in Functions


#Put Your AWS Credentials Below
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
    
    if request.method == 'POST':
        #Accessing the Recieved JSON Body To Access the Body parameters 
        data = request.get_json();
        
        body_str = data.get('body');
        #Get the Propmt From the Parameter
       
        body_data = json.loads(body_str);
        max_tokens = body_data.get('max_tokens_to_sample');
        
        #Accessing the Prompt From the Request Body
        prompt = body_data.get('prompt');
        
        # print(body_data.get('max_tokens_to_sample'))
        prompt_data = """Human:""" + prompt + """Assistant: """
        
        
        body = json.dumps({"prompt": prompt_data, "max_tokens_to_sample": max_tokens})
        modelId = data.get('modelId')  # change this to use a different version from the model provider
        accept = "application/json"
        contentType = data.get('contentType')
        
        try:
            response = boto3_bedrock.invoke_model(
                    body=body, modelId=modelId, accept=accept, contentType = contentType
                    );
            
            response_body = json.loads(response.get("body").read());
            return jsonify( {'Response': response_body.get("completion")});
        except Exception as err:
            print(err);
            return "Error While Invoking the AI Model";
        
    if request.method == 'GET':
        #Accessing the Prompt From the Request Body
        prompt = request.args.get('prompt');
        
        # print(body_data.get('max_tokens_to_sample'))
        prompt_data = f"""Human: {prompt}
        
        Assistant: 
        """
        
        max_tokens =int(request.args.get('max_tokens_to_sample'));
        model = request.args.get('modelId');

        print("Received Prompt is :","Received Prompt is :", prompt);
        print("Received Tokens are :", max_tokens);
        print("Received ModelId is :", model);
        
        body = json.dumps({"prompt": prompt_data, "max_tokens_to_sample": max_tokens})
        modelId = model  # change this to use a different version from the model provider
        accept = "application/json";
        contentType = "application/json";
        
        try:
            response = boto3_bedrock.invoke_model(
                    body=body, modelId=modelId, accept=accept, contentType = contentType
                    );
            
            response_body = json.loads(response.get("body").read());
            return  response_body.get("completion"); 
        except Exception as err:
            print(err);      
            return "Error While Invoking the AI Model."
    else:
        return "Please Send the GET Request. Thank You!"       
if __name__ == '__main__':
    app.run(debug=True)


# List the Available AI model in AWS BedRock

# models = boto3_bedrock.list_foundation_models();
# print(models)



