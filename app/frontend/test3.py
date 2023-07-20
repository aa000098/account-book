import gradio as gr
import pandas as pd
import boto3
import dotenv
import os
import io

file_name = 'AccountBook.csv'

dotenv.load_dotenv("C:/Users/손현호/account_book/app/frontend/.env", override=True)

def get_csv():
    global file_name
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket(os.getenv("BUCKET_NAME"))
    try:
        object = bucket.Object(file_name)
    except:
        df = pd.DataFrame(columns = ['분류','날짜','사용처','금액','카테고리','메모'])
        account_book = df.to_csv
        bucket.put_object(Body = account_book, Key = file_name)
        object = bucket.Object(file_name)
    csv_content = object.get()['Body'].read()
    account_book = pd.read_csv(io.BytesIO(csv_content))
    return account_book

def update_csv(csv_file):
    global file_name
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket(os.getenv("BUCKET_NAME"))
    bucket.put_object(Body = csv_file, Key = file_name)

def input_records(분류,날짜,사용처,금액,카테고리,메모):
    account_book = get_csv()
    new_record = pd.DataFrame([[분류, 날짜, 사용처, 금액, 카테고리, 메모]], columns=['분류', '날짜', '사용처', '금액', '카테고리', '메모'])
    account_book = pd.concat([account_book, new_record])
    update_csv(account_book)

account_book = get_csv()
update_csv(account_book)