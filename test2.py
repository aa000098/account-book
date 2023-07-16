import gradio as gr
import pandas as pd

# 임의의 데이터프레임 생성
data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Paris', 'London']
}
df = pd.DataFrame(data)

def modify_dataframe(name, age, city):
    # 데이터프레임 수정
    df.loc[df['Name'] == name, 'Age'] = age
    df.loc[df['Name'] == name, 'City'] = city
    return df

# Gradio 인터페이스 설정
name_input = gr.inputs.Dropdown(choices=df['Name'].tolist(), label="Name")
age_input = gr.inputs.Number(label="Age")
city_input = gr.inputs.Textbox(label="City")
output_text = gr.outputs.Textbox(label="Modified DataFrame")

def update_dataframe(name, age, city):
    modified_df = modify_dataframe(name, age, city)
    return modified_df.to_string(index=False)

# Gradio 인터페이스 실행
iface = gr.Interface(fn=update_dataframe, inputs=[name_input, age_input, city_input], outputs=output_text)
iface.launch()
