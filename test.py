import pandas as pd
import gradio as gr

# AccountBook.csv 파일을 데이터프레임으로 불러오기
file_path="AccountBook.csv"
account_book = pd.read_csv(file_path)

# 데이터프레임을 출력하는 함수
def view_records():
    return account_book

# Gradio 인터페이스 생성
def interface():
    with gr.Blocks() as app_interface:
        with gr.Tab("조회"):
            iface = gr.Interface(fn=view_records, 
                     title='Account Book Viewer', 
                     description='View Account Book DataFrame',
                     layout='wide',
                     inputs=None,  # 입력 없음
                     outputs="text")  # 출력 형식은 텍스트로 설정)
            iface.launch()

    app_interface.launch()

if __name__ == "__main__":
    interface()
