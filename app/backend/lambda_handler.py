import json
import boto3
import os
import dotenv

dotenv.load_dotenv("C:/Users/손현호/account_book/app/frontend/.env", override=True)

def create_file(event, context):
    session = boto3.Session()
    s3 = session.resource('s3')

    file_name = event['file_name']
    file_contents = event["file_contents"]

    object = s3.Object(os.getenv("BUCKET_NAME"), file_name)
    result = object.put(Body=file_contents)

    return {
        'statusCode' : 200,
        'body' : json.dumps(f'{file_name} saved!'),
        'file_contents' : file_contents
    }


def read_file(event, context):
    session = boto3.Session()
    s3 = session.resource('s3')

    file_name = event['file_name']

    object = s3.Object(os.getenv("BUCKET_NAME"), file_name)
    file_contents = object.get()["Body"].read().decode("utf-8")

    return {
        "statusCode" : 200,
        "body" : json.dumps(f"{file_name} read!"),
        "file_contents" : file_contents,
    }

def update_file(event, context):
    session = boto3.Session()
    s3 = session.resource('s3')

    file_name = event['file_name']
    file_contents = event["file_contents"]

    object = s3.Object(os.getenv("BUCKET_NAME"), file_name)
    file_contents = object.put(Body=file_contents)

    return {
        "statusCode" : 200,
        "body" : json.dumps(f"{file_name} update!"),
        "file_contents" : file_contents,
    }

def delete_file(event, context):
    session = boto3.Session()
    s3 = session.resource('s3')

    file_name = event['file_name']
    obj = s3.Object(os.getenv("BUCKET_NAME"), file_name)
    obj.delete()

    return {
        "statusCode" : 200,
        "body" : json.dumps(f"{file_name} update!"),
    }

def lambda_handler(event, context):
    if event['method'] == 'create':
        return create_file(event, context)
    elif event['method'] == 'read':
        return read_file(event, context)
    elif event['method'] == 'update':
        return update_file(event, context)
    elif event['method'] == 'delete':
        return delete_file(event, context)
    else:
        return {
            'satusCode':400,
            'body': json.dumps('Error')
        }