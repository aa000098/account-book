import json
import boto3
import os
import dotenv
import read_file

dotenv.load_dotenv("C:/Users/손현호/account_book/app/frontend/.env", override=True)


def create():
    df = pd.DataFrame(columns = ['분류','날짜','사용처','금액','카테고리','메모'])
    account_book = df.to_csv(index=False)
    bucket.put_object(Body = account_book, Key = file_name)
    return bucket.Object(file_name)

def lambda_handler(event, context):

    
    if event['httpMethod'] == 'GET':
        return read_file.lambda_handler(event, context)
    elif event['httpMethod'] == 'POST':
        return  
    