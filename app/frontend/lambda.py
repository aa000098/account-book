import gradio as gr
import pandas as pd
import json
import boto3
import io

# CSV 파일 이름
file_name = 'AccountBook.csv'
# 가계부 카테고리 드롭다운 옵션
dropdown_category = ["식비", "카페ㆍ간식", "편의점ㆍ마트ㆍ잡화", "술ㆍ유흥", "쇼핑", 
                     "취미ㆍ여가", "의료ㆍ건강ㆍ피트니스", "주거ㆍ통신", "보험ㆍ세금ㆍ기타금융", 
                     "미용", "교통ㆍ자동차", "여행ㆍ숙박", "교육", "생활", "기부ㆍ후원", 
                     "카테고리 없음", "ATM 출금", "이체", "급여", "저축ㆍ투자"]

# AWS Lambda 함수를 통해 CSV 파일 생성하는 함수
def create_csv(file_name):
    df = pd.DataFrame(columns = ['분류','날짜','사용처','금액','카테고리','메모'])
    account_book = df.to_csv(index=False)

    lambda_client = boto3.client("lambda")
    response = lambda_client.invoke(
        FunctionName = 'son-hyunho-ICN-handler-file',
        InvocationType = 'RequestResponse',
        Payload = json.dumps({
            "method" : "create",
            "file_name" : file_name,
            "file_contents" : account_book
        })
    )
    response_payload = json.loads(response["Payload"].read().decode('utf-8'))
    return response_payload
    
# AWS Lambda 함수를 통해 CSV 파일 읽어오는 함수
def get_csv(file_name):
    lambda_client = boto3.client("lambda")
    response = lambda_client.invoke(
        FunctionName = 'son-hyunho-ICN-handler-file',
        InvocationType = 'RequestResponse',
        Payload = json.dumps({
            "method" : "read",
            "file_name" : file_name,
        })
    )
    response_payload = json.loads(response["Payload"].read().decode('utf-8'))

    if 'statusCode' not in response_payload or response_payload["statusCode"] != 200:
        response_payload = create_csv(file_name)
    
    csv_content = response_payload['file_contents']
    csv_bytes = bytes(csv_content, 'utf-8')
    account_book = pd.read_csv(io.BytesIO(csv_bytes))
    return account_book

# AWS Lambda 함수를 통해 CSV 파일 업데이트하는 함수
def update_csv(file_name, account_book):
    csv_file = account_book.to_csv(index=False)
    
    lambda_client = boto3.client("lambda")
    response = lambda_client.invoke(
        FunctionName = 'son-hyunho-ICN-handler-file',
        InvocationType = 'RequestResponse',
        Payload = json.dumps({
            "method" : "update",
            "file_name" : file_name,
            "file_contents" : csv_file
        })
    )

# AWS Lambda 함수를 통해 CSV 파일 삭제하는 함수
def delete_csv():
    global file_name
    lambda_client = boto3.client("lambda")
    response = lambda_client.invoke(
        FunctionName = 'son-hyunho-ICN-handler-file',
        InvocationType = 'RequestResponse',
        Payload = json.dumps({
            "method" : "delete",
            "file_name" : file_name,
        })
    )

#-----------------------------------------------
# 가계부 조회 기능
def view_records():
    global file_name
    return get_csv(file_name)

# 가계부 입력 기능
def input_records(분류,날짜,사용처,금액,카테고리,메모):
    global file_name
    account_book = get_csv(file_name)
    new_record = pd.DataFrame([[분류, 날짜, 사용처, 금액, 카테고리, 메모]], 
                              columns=['분류', '날짜', '사용처', '금액', '카테고리', '메모'])
    account_book = pd.concat([account_book, new_record])
    update_csv(file_name, account_book)

# 가계부 수정 기능
def correct_records(인덱스,분류,날짜,사용처,금액,카테고리,메모):
    global file_name
    account_book = get_csv(file_name)
    if (인덱스<1) or (인덱스>account_book.shape[0]):
        return 0
    else:
        account_book.loc[인덱스-1] = [분류,날짜,사용처,금액,카테고리,메모]
        update_csv(file_name, account_book)

# 가계부 인덱스 보기 기능
def view_index():
    global file_name
    account_book = get_csv(file_name)
    df_with_index = account_book.reset_index()
    df_with_index.columns = ['인덱스'] + list(account_book.columns)
    df_with_index['인덱스'] += 1
    return df_with_index

# 가계부 삭제 기능
def delete_records(인덱스):
    global file_name
    account_book = get_csv(file_name)
    if (인덱스<1) or (인덱스>account_book.shape[0]):
        val = pd.DataFrame()
    else:
        val = account_book.loc[인덱스-1].to_frame().T
        account_book.drop(인덱스-1, axis=0, inplace=True)
        update_csv(file_name, account_book)
    return val

# 가계부 조회 인터페이스
def 조회():
    gr.Interface(fn = view_records, inputs=None, outputs="dataframe", 
                                  title="가계부", allow_flagging='never', live=True)

# 가계부 입력 인터페이스
def 입력():
    분류 = gr.Radio(["수입", "지출"], label="분류")
    날짜 = gr.Textbox(label="날짜",placeholder="YYYY-MM-DD")
    사용처 = gr.Textbox(label="사용처", placeholder="사용처")
    금액 = gr.Number(label="금액")
    카테고리 = gr.Dropdown(dropdown_category, label="카테고리")
    메모 = gr.Textbox(label="메모", placeholder="메모를 남겨보세요")
    input_button = gr.Button("입력하기")
    input_button.click(input_records, inputs=([분류,날짜,사용처,금액,카테고리,메모]), outputs=None)
  
# 가계부 수정 인터페이스  
def 수정():
    인덱스 = gr.Number(label="수정하고 싶은 데이터의 인덱스")
    분류 = gr.Radio(["수입", "지출"], label="분류")
    날짜 = gr.Textbox(label="날짜",placeholder="YYYY-MM-DD")
    사용처 = gr.Textbox(label="사용처", placeholder="사용처")
    금액 = gr.Number(label="금액")
    카테고리 = gr.Dropdown(dropdown_category, label="카테고리")
    메모 = gr.Textbox(label="메모", placeholder="메모를 남겨보세요")
    correction_button = gr.Button("수정하기")
    correction_button.click(correct_records, inputs=([인덱스,분류,날짜,사용처,금액,카테고리,메모]), outputs=None)
    gr.Interface(fn = view_index, inputs=None, outputs="dataframe", 
                                   title="가계부", allow_flagging='never', live=True)

# 가계부 삭제 인터페이스
def 삭제():
    gr.Interface(fn=delete_records, 
                 inputs="number", 
                 outputs="dataframe", 
                 allow_flagging='never')

# 가계부 삭제 기능 인터페이스
def 가계부_삭제():
    global file_name
    del_button = gr.Button("가계부 삭제하기")
    del_button.click(delete_csv)

# 메인 인터페이스
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
        with gr.Tab("가계부 삭제"):
            가계부_삭제()
        
    app_interface.launch()

if __name__ == "__main__":
    interface()
