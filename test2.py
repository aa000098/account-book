import gradio as gr
import pandas as pd


file_path="AccountBook.csv"
account_book = pd.read_csv(file_path)

print(account_book.loc[1].to_frame().T)