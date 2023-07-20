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
        account_book = df.to_csv(index=False)
        bucket.put_object(Body = account_book, Key = file_name)
        object = bucket.Object(file_name)
    csv_content = object.get()['Body'].read()
    account_book = pd.read_csv(io.BytesIO(csv_content))
    return account_book

def update_csv(account_book):
    global file_name
    csv_file = account_book.to_csv(index=False)
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket(os.getenv("BUCKET_NAME"))
    bucket.put_object(Body = csv_file, Key = file_name)

#-----------------------------------------------
def view_records():
    return get_csv()

def input_records(분류,날짜,사용처,금액,카테고리,메모):
    account_book = get_csv()
    new_record = pd.DataFrame([[분류, 날짜, 사용처, 금액, 카테고리, 메모]], columns=['분류', '날짜', '사용처', '금액', '카테고리', '메모'])
    account_book = pd.concat([account_book, new_record])
    update_csv(account_book)

def correct_records(인덱스,분류,날짜,사용처,금액,카테고리,메모):
    account_book = get_csv()
    if (인덱스<1) or (인덱스>account_book.shape[0]):
        return 0
    else:
        account_book.loc[인덱스-1] = [분류,날짜,사용처,금액,카테고리,메모]
        update_csv(account_book)

def view_index():
    account_book = get_csv()
    df_with_index = account_book.reset_index()
    df_with_index.columns = ['인덱스'] + list(account_book.columns)
    df_with_index['인덱스'] += 1
    return df_with_index

def delete_records(인덱스):
    account_book = get_csv()
    if (인덱스<1) or (인덱스>account_book.shape[0]):
        val = pd.DataFrame()
    else:
        val = account_book.loc[인덱스-1].to_frame().T
        account_book.drop(인덱스-1, axis=0, inplace=True)
        update_csv(account_book)
    return val

def 조회():
    view_interface = gr.Interface(fn = view_records, inputs=None, outputs="dataframe", title="가계부", allow_flagging='never', live=True)

def 입력():
    분류 = gr.Radio(["수입", "지출"], label="분류")
    날짜 = gr.Textbox(label="날짜",placeholder="YYYY-MM-DD")
    사용처 = gr.Textbox(label="사용처", placeholder="사용처")
    금액 = gr.Number(label="금액")
    카테고리 = gr.Dropdown(["식비", "카페ㆍ간식", "편의점ㆍ마트ㆍ잡화", "술ㆍ유흥", "쇼핑", "취미ㆍ여가", "의료ㆍ건강ㆍ피트니스", "주거ㆍ통신", "보험ㆍ세금ㆍ기타금융", "미용", "교통ㆍ자동차", "여행ㆍ숙박", "교육", "생활", "기부ㆍ후원", "카테고리 없음", "ATM 출금", "이체", "급여", "저축ㆍ투자"], label="카테고리")
    메모 = gr.Textbox(label="메모", placeholder="메모를 남겨보세요")
    input_button = gr.Button("입력하기")
    input_button.click(input_records, inputs=([분류,날짜,사용처,금액,카테고리,메모]), outputs=None)
    
def 수정():
    인덱스 = gr.Number(label="수정하고 싶은 데이터의 인덱스")
    분류 = gr.Radio(["수입", "지출"], label="분류")
    날짜 = gr.Textbox(label="날짜",placeholder="YYYY-MM-DD")
    사용처 = gr.Textbox(label="사용처", placeholder="사용처")
    금액 = gr.Number(label="금액")
    카테고리 = gr.Dropdown(["식비", "카페ㆍ간식", "편의점ㆍ마트ㆍ잡화", "술ㆍ유흥", "쇼핑", "취미ㆍ여가", "의료ㆍ건강ㆍ피트니스", "주거ㆍ통신", "보험ㆍ세금ㆍ기타금융", "미용", "교통ㆍ자동차", "여행ㆍ숙박", "교육", "생활", "기부ㆍ후원", "카테고리 없음", "ATM 출금", "이체", "급여", "저축ㆍ투자"], label="카테고리")
    메모 = gr.Textbox(label="메모", placeholder="메모를 남겨보세요")
    correction_button = gr.Button("수정하기")
    correction_button.click(correct_records, inputs=([인덱스,분류,날짜,사용처,금액,카테고리,메모]), outputs=None)
    index_interface = gr.Interface(fn = view_index, inputs=None, outputs="dataframe", title="가계부", allow_flagging='never', live=True)

def 삭제():
    gr.Interface(fn=delete_records, inputs="number", outputs="dataframe", allow_flagging='never')

def interface():
    with gr.Blocks() as app_interface:
        with gr.Tab("조회"):
            조회()
        with gr.Tab("입력"):
            입력()
        with gr.Tab("수정"):
            수정()
        with gr.Tab("삭제"):
            삭제()
        
    app_interface.launch()

if __name__ == "__main__":
    interface()
