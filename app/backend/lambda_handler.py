import json
import boto3
import os

def create_file(event, context):
    # AWS Session과 S3 리소스를 생성
    session = boto3.Session()
    s3 = session.resource('s3')

    # 이벤트에서 파일 이름과 내용을 가져옴
    file_name = event['file_name']
    file_contents = event["file_contents"]

    # S3 버킷에 파일을 생성하고 내용을 저장
    object = s3.Object(os.getenv("BUCKET_NAME"), file_name)
    result = object.put(Body=file_contents)

    # 성공적으로 파일을 생성했음을 반환
    return {
        'statusCode' : 200,
        'body' : json.dumps(f'{file_name} saved!'),
        'file_contents' : file_contents
    }


def read_file(event, context):
    session = boto3.Session()
    s3 = session.resource('s3')

    file_name = event['file_name']

    # S3 버킷에서 파일 내용을 읽어옴
    object = s3.Object(os.getenv("BUCKET_NAME"), file_name)
    file_contents = object.get()["Body"].read().decode("utf-8")

    # 성공적으로 파일을 읽었음을 파일 콘텐츠와 함께 반환
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

    # S3 버킷에 파일을 업데이트하고 내용을 저장
    object = s3.Object(os.getenv("BUCKET_NAME"), file_name)
    result = object.put(Body=file_contents)

    return {
        "statusCode" : 200,
        "body" : json.dumps(f"{file_name} update!"),
    }

def delete_file(event, context):
    session = boto3.Session()
    s3 = session.resource('s3')

    file_name = event['file_name']

    # S3 버킷에서 파일을 삭제
    object = s3.Object(os.getenv("BUCKET_NAME"), file_name)
    result = object.delete()

    return {
        "statusCode" : 200,
        "body" : json.dumps(f"{file_name} update!"),
    }

def lambda_handler(event, context):
    # 메소드에 따라 적절한 함수 호출
    if event['method'] == 'create':
        return create_file(event, context)
    elif event['method'] == 'read':
        return read_file(event, context)
    elif event['method'] == 'update':
        return update_file(event, context)
    elif event['method'] == 'delete':
        return delete_file(event, context)
    else:
        # 잘못된 메소드 요청된 경우 오류 반환
        return {
            'satusCode':400,
            'body': json.dumps('Error')
        }