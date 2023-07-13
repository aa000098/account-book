import gradio as gr
import requests
import pandas

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()


def sum(a,b):
    c = a + b
    return c


# API 사용법
# requests.get(url="")
# pandas로 테이블로 만들어서 
# # jason형식으로 해석
# dataframe으로 가공


iface = gr.Interface(sum, input = {"number", "number"}, outputs={"text"})
# 입출력의 개수와 타입이 맞아야 함
iface.launch