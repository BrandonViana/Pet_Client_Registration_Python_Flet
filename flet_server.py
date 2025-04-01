import flet as ft

def main(page: ft.Page):
    page.title = "Cadastro de Clientes"
    page.add(ft.Text("Bem-vindo ao Cadastro de Clientes!"))

ft.app(target=main, view=ft.AppView.WEB)