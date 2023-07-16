import gradio as gr
import pandas as pd
import csv

file_path="AccountBook.csv"
account_book = pd.read_csv(file_path)

def view_records():
    return account_book

def input_records(분류,날짜,사용처,금액,카테고리,메모):
    global account_book
    new_record = pd.DataFrame([[분류, 날짜, 사용처, 금액, 카테고리, 메모]], columns=['분류', '날짜', '사용처', '금액', '카테고리', '메모'])
    account_book = pd.concat([account_book, new_record])
    account_book.to_csv(file_path, index=False)


def interface():
    with gr.Blocks() as app_interface:
        with gr.Tab("조회"):
            view_interface = gr.Interface(fn = view_records, inputs=None, outputs="dataframe", title="가계부")
        
        with gr.Tab("입력"):
            분류 = gr.Radio(["수입", "지출"], label="분류")
            날짜 = gr.Textbox(label="날짜",placeholder="YYYY-MM-DD")
            사용처 = gr.Textbox(label="사용처", placeholder="사용처")
            금액 = gr.Number(label="금액")
            카테고리 = gr.Dropdown(["식비", "카페ㆍ간식", "편의점ㆍ마트ㆍ잡화", "술ㆍ유흥", "쇼핑", "취미ㆍ여가", "의료ㆍ건강ㆍ피트니스", "주거ㆍ통신", "보험ㆍ세금ㆍ기타금융", "미용", "교통ㆍ자동차", "여행ㆍ숙박", "교육", "생활", "기부ㆍ후원", "카테고리 없음", "ATM 출금", "이체", "급여", "저축ㆍ투자"], label="카테고리")
            메모 = gr.Textbox(label="메모", placeholder="메모를 남겨보세요")
            input_button = gr.Button("입력하기")
            input_button.click(input_records, inputs=([분류,날짜,사용처,금액,카테고리,메모]), outputs=None)

            

    app_interface.launch()

if __name__ == "__main__":
    interface()
