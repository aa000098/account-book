import gradio as gr
import pandas as pd

file_path="C:/Users/손현호/account_book/app/frontend/AccountBook.csv"
account_book = pd.read_csv(file_path)



def input_records(분류,날짜,사용처,금액,카테고리,메모):
    account_book = pd.read_csv(file_path)
    new_record = pd.DataFrame([[분류, 날짜, 사용처, 금액, 카테고리, 메모]], columns=['분류', '날짜', '사용처', '금액', '카테고리', '메모'])
    account_book = pd.concat([account_book, new_record])
    account_book.to_csv(file_path, index=False)

def correct_records(인덱스,분류,날짜,사용처,금액,카테고리,메모):
    account_book = pd.read_csv(file_path)
    if (인덱스<1) or (인덱스>account_book.shape[0]):
        return 0
    else:
        account_book.loc[인덱스-1] = [분류,날짜,사용처,금액,카테고리,메모]
        account_book.to_csv(file_path, index=False)

def view_index():
    account_book = pd.read_csv(file_path)
    df_with_index = account_book.reset_index()
    df_with_index.columns = ['인덱스'] + list(account_book.columns)
    df_with_index['인덱스'] += 1
    return df_with_index

def delete_records(인덱스):
    account_book = pd.read_csv(file_path)
    if (인덱스<1) or (인덱스>account_book.shape[0]):
        val = pd.DataFrame()
    else:
        val = account_book.loc[인덱스-1].to_frame().T
        account_book.drop(인덱스-1, axis=0, inplace=True)
        account_book.to_csv(file_path, index=False)
    return val

def view_records():
    account_book = pd.read_csv(file_path)
    return account_book

def interface():
    with gr.Blocks as app:
        view = gr.Interface(fn=view_index, inputs=None, outputs="dataframe", title="가계부", allow_flagging='never', live=True)
        write = gr.Interface(fn = input_records, 
                         inputs = (gr.Radio(["수입", "지출"], label="분류"),
                                    gr.Textbox(label="날짜",placeholder="YYYY-MM-DD"),
                                    gr.Textbox(label="사용처", placeholder="사용처"),
                                    gr.Number(label="금액"),
                                    gr.Dropdown(["식비", "카페ㆍ간식", "편의점ㆍ마트ㆍ잡화", "술ㆍ유흥", "쇼핑", "취미ㆍ여가", "의료ㆍ건강ㆍ피트니스", "주거ㆍ통신", "보험ㆍ세금ㆍ기타금융", "미용", "교통ㆍ자동차", "여행ㆍ숙박", "교육", "생활", "기부ㆍ후원", "카테고리 없음", "ATM 출금", "이체", "급여", "저축ㆍ투자"], label="카테고리"),
                                    gr.Textbox(label="메모", placeholder="메모를 남겨보세요")),
                        outputs=None)
        correct = gr.Interface(fn = correct_records, 
                           inputs = (gr.Number(label="수정하고 싶은 데이터의 인덱스"),
                                    gr.Radio(["수입", "지출"], label="분류"),
                                    gr.Textbox(label="날짜",placeholder="YYYY-MM-DD"),
                                    gr.Textbox(label="사용처", placeholder="사용처"),
                                    gr.Number(label="금액"),
                                    gr.Dropdown(["식비", "카페ㆍ간식", "편의점ㆍ마트ㆍ잡화", "술ㆍ유흥", "쇼핑", "취미ㆍ여가", "의료ㆍ건강ㆍ피트니스", "주거ㆍ통신", "보험ㆍ세금ㆍ기타금융", "미용", "교통ㆍ자동차", "여행ㆍ숙박", "교육", "생활", "기부ㆍ후원", "카테고리 없음", "ATM 출금", "이체", "급여", "저축ㆍ투자"], label="카테고리"),
                                    gr.Textbox(label="메모", placeholder="메모를 남겨보세요")),
                            outputs = None)
        delete = gr.Interface(fn=delete_records, inputs="number", outputs="dataframe", allow_flagging='never')

    app.launch()


if __name__ == "__main__":
    interface()
