import json
import boto3
import os
import dotenv

dotenv.load_dotenv("C:/Users/손현호/account_book/app/frontend/.env", override=True)


def create_file():
    df = pd.DataFrame(columns = ['분류','날짜','사용처','금액','카테고리','메모'])
    account_book = df.to_csv(index=False)
    bucket.put_object(Body = account_book, Key = file_name)
    return bucket.Object(file_name)

def read_file():

    return 

def update_file():
    return

def delete_file():
    return

def lambda_handler(event, context):
    if event['method'] == 'create':
        return create_file.lambda_handler(event, context)
    elif event['method'] == 'read':
        return read_file 
    elif event['method'] == 'update':
        return update_file
    elif event['method'] == 'delete':
        return delete_file
    else:
        return {
            'satusCode':400,
            'body': json.dumps('Error')
        }