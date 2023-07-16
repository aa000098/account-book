import gradio as gr
import pandas as pd
import csv

file_path="AccountBook.csv"
account_book = pd.read_csv(file_path)

def view_records():
    return account_book

def input_records(분류,날짜,항목,금액,카테고리,메모):
    global account_book
    new_record = pd.DataFrame([[분류, 날짜, 항목, 금액, 카테고리, 메모]], columns=['분류', '날짜', '항목', '금액', '카테고리', '메모'])
    account_book = account_book.append(new_record, index=True)
    account_book.to_csv(file_path, index=True)


def interface():
    with gr.Blocks("가계부") as app_interface:
        with gr.Tab("조회"):
            view_interface = gr.Interface(rf = view_records, label = "조회", inputs=None, outputs="dataframe")
            view_interface.launch()

        with gr.Tab("입력"):
            input_text = gr.Interface(fn=input_records, inputs=[gr.Checkbox("수입"),
                                                                gr.Checkbox("지출"), 
                                                                "text", "text", "text", "number", "text", "text"],
                                                                outputs=None, title="가계부 입력")
            input_text.launch()

        with gr.Tab("수정"):
            input_text = gr.Interface(fn=input_records, inputs=[gr.Checkbox("수입"),
                                                                gr.Checkbox("지출"), 
                                                                "text", "text", "text", "number", "text", "text"],
                                                                outputs=None, title="가계부 입력")
            input_text.launch()

        with gr.Tab("삭제"):
            input_text = gr.Interface(fn=input_records, inputs=[gr.Checkbox("수입"),
                                                                gr.Checkbox("지출"), 
                                                                "text", "text", "text", "number", "text", "text"],
                                                                outputs=None, title="가계부 입력")
            input_text.launch()

    app_interface.launch()

if __name__ == "__main__":
    interface()