import os
import boto3
import json

boto3_session = boto3.session.Session()
region = boto3_session.region_name

# create a boto3 bedrock client
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

# get knowledge base id from environment variable
kb_id = os.environ.get("KNOWLEDGE_BASE_ID")

# declare model id for calling RetrieveAndGenerate API
model_id = "anthropic.claude-v2:1"
model_arn = f'arn:aws:bedrock:{region}::foundation-model/{model_id}'


def retrieveAndGenerate(input, kbId, model_arn, sessionId=None):
    print(input, kbId, model_arn)
    if sessionId != "None":
        return bedrock_agent_runtime_client.retrieve_and_generate(
            input={
                'text': input
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kbId,
                    'modelArn': model_arn
                }
            },
            sessionId=sessionId
        )
    else:
        return bedrock_agent_runtime_client.retrieve_and_generate(
            input={
                'text': input
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kbId,
                    'modelArn': model_arn
                }
            }
        )


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        query = body["question"]
        session_id = body["sessionid"]

        # log all the incoming details
        print(f"Query: {query}")
        print(f"Session ID: {session_id}")


        response = retrieveAndGenerate(query, kb_id, model_arn, session_id)
        print(response)
        generated_text = response['output']['text']
        print(generated_text)

        return {
            'statusCode': 200,
            'body': {"question": query.strip(), "answer": generated_text.strip()}
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }