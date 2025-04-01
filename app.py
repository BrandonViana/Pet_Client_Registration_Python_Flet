import flet as ft
import os
import csv
from formatters import formatar_celular, formatar_horario, formatar_data, formatar_dinheiro, formatar_nome_pet


def main(page: ft.Page):
    checkboxes = {}

    global data_table
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("✔️")),
            ft.DataColumn(ft.Text("Data", color="white")),
            ft.DataColumn(ft.Text("Nome", color="white")),
            ft.DataColumn(ft.Text("Celular", color="white")),
            ft.DataColumn(ft.Text("Horário", color="white")),
            ft.DataColumn(ft.Text("Pet", color="white")),
            ft.DataColumn(ft.Text("Sexo", color="white")),
            ft.DataColumn(ft.Text("Serviço", color="white")),
            ft.DataColumn(ft.Text("Observações", color="white")),
            ft.DataColumn(ft.Text("Pagamento", color="white")),
            ft.DataColumn(ft.Text("Valor", color="white")),
        ],
        rows=[]
    )
    page.title = "Cadastro de Clientes Pet Belize"
    BG = "#004173"
    FG = "#89CFF0"
    AZUL_CLARO = "#ADD8E6"

    def abrir_menu(e):
        ft.Container = pagina_principal.controls[0]
        ft.Container.width = 200
        ft.Container.scale = ft.transform.Scale(
            0.8, alignment=ft.alignment.center_right)
        ft.Container.border_radius = ft.border_radius.only(
            top_left=35,
            top_right=0,
            bottom_left=35,
            bottom_right=0
        )
        ft.Container.update()

    def abrir_menu_secundario(e):
        ft.Container = pagina_secundaria.controls[0]
        ft.Container.width = 200
        ft.Container.scale = ft.transform.Scale(
            0.8, alignment=ft.alignment.center_right)
        ft.Container.border_radius = ft.border_radius.only(
            top_left=35,
            top_right=0,
            bottom_left=35,
            bottom_right=0
        )
        ft.Container.update()

    def restore_menu(e):
        ft.Container = pagina_principal.controls[0]
        ft.Container.width = 400
        ft.Container.scale = ft.transform.Scale(
            1, alignment=ft.alignment.center_right)
        ft.Container.update()
        pagina_principal.update()

    def restore_menu_secundario(e):
        ft.Container = pagina_secundaria.controls[0]
        ft.Container.width = 400
        ft.Container.scale = ft.transform.Scale(
            1, alignment=ft.alignment.center_right)
        ft.Container.update()
        pagina_secundaria.update()

    def pagina_historico(e):
        restore_menu_secundario(e)
        carregar_dados()
        pagina_secundaria.visible = True
        pagina_principal.visible = False
        page.update()

    def pagina_principal_view(e):
        restore_menu(e)
        pagina_secundaria.visible = False
        pagina_principal.visible = True
        page.update()

    def atualizar_dias(e):
        mes_selecionado = dropdown_mes.value
        dias = range(1, dias_por_mes[mes_selecionado] + 1)

        dropdown_dia.options = [ft.dropdown.Option(str(dia)) for dia in dias]
        dropdown_dia.update()

    def cadastrar(e):
        checkbox = ft.Checkbox(value=False)
        nova_linha = ft.DataRow(
            cells=[
                ft.DataCell(checkbox),
                ft.DataCell(ft.Text(data_input.value, color="white")),
                ft.DataCell(ft.Text(nome_cliente_input.value, color="white")),
                ft.DataCell(ft.Text(celular_input.value, color="white")),
                ft.DataCell(ft.Text(horario_input.value, color="white")),
                ft.DataCell(ft.Text(nome_pet_input.value, color="white")),
                ft.DataCell(
                    ft.Text(sexo_dropdown.value if sexo_dropdown.value else "-", color="white")),
                ft.DataCell(ft.Text(
                    servicos_dropdown.value if servicos_dropdown.value else "-", color="white")),
                ft.DataCell(ft.Text(
                    observacoes_input.value if observacoes_input.value else "-", color="white")),
                ft.DataCell(ft.Text(
                    pagamento_dropdown.value if pagamento_dropdown.value else "-", color="white")),
                ft.DataCell(ft.Text(dinheiro_input.value, color="white")),
            ]
        )

        data_table.rows.append(nova_linha)

        checkboxes[nova_linha] = checkbox

        data_table.update()

        salvar_dados()

    def salvar_dados():
        arquivo_csv = "Histórico.csv"

        existe = os.path.exists(arquivo_csv)

        with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not existe:
                writer.writerow(["Data", "Nome", "Celular", "Horário", "Pet",
                                "Sexo", "Serviço", "Observações", "Pagamento", "Valor"])

            writer.writerow([
                data_input.value,
                nome_cliente_input.value,
                celular_input.value,
                horario_input.value,
                nome_pet_input.value,
                sexo_dropdown.value if sexo_dropdown.value else "-",
                servicos_dropdown.value if servicos_dropdown.value else "-",
                observacoes_input.value if observacoes_input.value else "-",
                pagamento_dropdown.value if pagamento_dropdown.value else "-",
                dinheiro_input.value
            ]
            )

    def carregar_dados():
        arquivo_csv = "Histórico.csv"

        if not os.path.exists(arquivo_csv):
            return

        data_table.rows.clear()
        checkboxes.clear()

        with open(arquivo_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)

            for linha in reader:
                checkbox = ft.Checkbox(value=False)
                nova_linha = ft.DataRow(
                    cells=[
                        ft.DataCell(checkbox),
                        *[ft.DataCell(ft.Text(d, color="white")) for d in linha]
                    ]
                )
                data_table.rows.append(nova_linha)
                checkboxes[nova_linha] = checkbox
        data_table.update()

    def buscar_dados_cliente(e):
        e.control.value = e.control.value.title()
        e.control.update()
        nome_digitado = nome_cliente_input.value.strip()
        if not nome_digitado:
            return

        arquivo_csv = "Histórico.csv"

        if not os.path.exists(arquivo_csv):
            return

        with open(arquivo_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)

            for linha in reader:
                nome_no_csv = linha[1].strip()

                if nome_digitado.lower() == nome_no_csv.lower():
                    celular_input.value = linha[2]
                    horario_input.value = linha[3]
                    nome_pet_input.value = linha[4]
                    sexo_dropdown.value = linha[5] if linha[5] != "-" else None
                    servicos_dropdown.value = linha[6] if linha[6] != "-" else None
                    observacoes_input.value = linha[7] if linha[7] != "-" else None
                    pagamento_dropdown.value = linha[8] if linha[8] != "-" else None
                    dinheiro_input.value = linha[9]

                    celular_input.update()
                    horario_input.update()
                    nome_pet_input.update()
                    sexo_dropdown.update()
                    servicos_dropdown.update()
                    observacoes_input.update()
                    pagamento_dropdown.update()
                    dinheiro_input.update()
                    break

    def filtrar_por_data(e):
        if not (dropdown_mes.value and dropdown_dia.value and dropdown_ano.value):
            return
        mes = meses.get(dropdown_mes.value, "").zfill(2)
        dia = dropdown_dia.value.zfill(2)
        ano = dropdown_ano.value

        if not mes:
            return

        data_filtrada = f"{dia}/{mes}/{ano}"

        arquivo_csv = "Histórico.csv"

        if not os.path.exists(arquivo_csv):
            return

        data_table.rows.clear()
        checkboxes.clear()
        encontrou = False

        with open(arquivo_csv, mode="r", newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader)

            for linha in reader:
                data_no_csv = linha[0].strip()

                if data_no_csv == data_filtrada:
                    encontrou = True

                    checkbox = ft.Checkbox(value=False)
                    nova_linha = ft.DataRow(
                        cells=[
                            ft.DataCell(checkbox),
                            *[ft.DataCell(ft.Text(d, color="white")) for d in linha]
                        ]
                    )
                    data_table.rows.append(nova_linha)
                    checkboxes[nova_linha] = checkbox

        data_table.update()

    def saida(e):
        arquivo_csv = "Histórico.csv"

        if not os.path.exists(arquivo_csv):
            return

        linhas_selecionadas = [
            [cell.content.value for cell in linha.cells[1:]]
            for linha, checkbox in checkboxes.items() if checkbox.value
        ]

        if not linhas_selecionadas:
            return

        with open(arquivo_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            cabecalho = next(reader)
            linhas_restantes = [
                linha for linha in reader if linha not in linhas_selecionadas]

        with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cabecalho)
            writer.writerows(linhas_restantes)

        for linha in list(checkboxes.keys()):
            if checkboxes[linha].value:
                data_table.rows.remove(linha)
                del checkboxes[linha]

        data_table.update()

    nome_cliente_text = ft.Text(value="Nome do(a) cliente:", font_family="Arial",
                                size=15, color="white", weight=ft.FontWeight.BOLD)
    nome_cliente_input = ft.TextField(
        hint_text="Digite o nome do(a) cliente...",
        color="white",
        expand=True,
        border_color="white",
        cursor_color="white",
        hint_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        max_length=50,
        on_change=buscar_dados_cliente
    )

    celular_text = ft.Text(
        value="Celular:",
        font_family="Arial",
        size=15,
        color="white",
        weight=ft.FontWeight.BOLD
    )
    celular_input = ft.TextField(
        hint_text="(00) 00000-0000",
        width=180,
        border_color="white",
        cursor_color="white",
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color="white"),
        max_length=15,
        on_change=formatar_celular
    )

    data_text = ft.Text(value="Data:", font_family="Arial",
                        size=15, color="white", weight=ft.FontWeight.BOLD)
    data_input = ft.TextField(
        hint_text="DD/MM/AAAA",
        width=120,
        border_color="white",
        cursor_color="white",
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color="white"),
        max_length=10,
        on_change=formatar_data
    )

    horario_text = ft.Text(value="Horário:", font_family="Arial",
                           size=15, color="white", weight=ft.FontWeight.BOLD)
    horario_input = ft.TextField(
        hint_text="00:00",
        width=100,
        border_color="white",
        cursor_color="white",
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color="white"),
        max_length=5,
        on_change=formatar_horario
    )

    nome_pet_text = ft.Text(
        value="Nome do Pet:",
        font_family="Arial",
        size=15,
        color="white",
        weight=ft.FontWeight.BOLD
    )
    nome_pet_input = ft.TextField(
        hint_text="Digite o nome do Pet...",
        color="white",
        expand=True,
        border_color="white",
        cursor_color="white",
        hint_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        max_length=30,
        on_change=formatar_nome_pet,
        width=200
    )

    sexo_text = ft.Text(value="Sexo:", font_family="Arial",
                        size=15, color="white", weight=ft.FontWeight.BOLD)
    sexo_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Macho"),
            ft.dropdown.Option("Fêmea")
        ],
        bgcolor=FG,
        text_style=ft.TextStyle(color="white"),
        hint_text="Selecione...",
        hint_style=ft.TextStyle(color="white"),
        color="white",
        text_size=10,
        border_color="white",
        border_radius=5,
        border_width=1,
        width=120
    )

    servicos_text = ft.Text(
        "Serviços", size=15, color="white", weight=ft.FontWeight.BOLD
    )
    servicos_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Banho"),
            ft.dropdown.Option("Banho c/ Tosa Higiênica"),
            ft.dropdown.Option("Tosa Geral"),
            ft.dropdown.Option("Tosa Bebê"),
            ft.dropdown.Option("Tosa da Raça"),
            ft.dropdown.Option("Desembolo"),
            ft.dropdown.Option("Hidratação"),
            ft.dropdown.Option("Outro")
        ],
        text_size=10,
        bgcolor=FG,
        color="white",
        border_color="white",
        text_style=ft.TextStyle(color="white"),
        hint_text="Selecione...",
        border_radius=5,
        border_width=1,
        width=150,
        hint_style=ft.TextStyle(color="white"),
    )
    servicos_textfield = ft.TextField(
        hint_text="Outro...",
        text_size=10,
        width=100,
        border_color="white",
        cursor_color="white",
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color="white"),
        border_radius=5,
        border_width=1
    )

    observacoes_text = ft.Text(
        "Observações:", size=20, color="white", weight=ft.FontWeight.BOLD)
    observacoes_input = ft.TextField(
        hint_text="Obs...",
        color="white",
        expand=True,
        border_color="white",
        cursor_color="white",
        hint_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        width=300
    )

    pagamento_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("PIX"),
            ft.dropdown.Option("Dinheiro"),
            ft.dropdown.Option("Débito"),
            ft.dropdown.Option("Crédito")
        ],
        bgcolor=FG,
        color="white",
        text_style=ft.TextStyle(color="white"),
        hint_text="Pagamento",
        hint_style=ft.TextStyle(color="white"),
        border_color="white",
        border_radius=5,
        border_width=1,
        width=150
    )

    dinheiro_input = ft.TextField(
        value="R$ 0,00",
        text_align=ft.TextAlign.RIGHT,
        width=120,
        border_color="white",
        cursor_color="white",
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color="white"),
        on_change=formatar_dinheiro
    )

    cadastrar_botao = ft.ElevatedButton(
        text="Cadastrar",
        bgcolor=FG,
        color="white",
        width=100,
        height=50,
        on_click=cadastrar
    )

    filtrar_dados = ft.ElevatedButton(
        text="Filtrar",
        bgcolor="white",
        color=FG,
        width=70,
        height=45,
        on_click=filtrar_por_data
    )
    botao_saida = ft.ElevatedButton(
        "Saída", on_click=saida,
        bgcolor=FG,
        color="white",
        width=100,
        height=50
    )

    anos = ["2025", "2026", "2027"]
    dias_por_mes = {
        "Janeiro": 31, "Fevereiro": 28, "Março": 31, "Abril": 30,
        "Maio": 31, "Junho": 30, "Julho": 31, "Agosto": 31,
        "Setembro": 30, "Outubro": 31, "Novembro": 30, "Dezembro": 31
    }
    meses = {
        "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04",
        "Maio": "05", "Junho": "06", "Julho": "07", "Agosto": "08",
        "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
    }

    dropdown_ano = ft.Dropdown(
        options=[ft.dropdown.Option(ano) for ano in anos],
        label="Ano",
        width=120,
        bgcolor=FG,
        color="white",
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color="white"),
        border_color="white",
    )

    dropdown_mes = ft.Dropdown(
        options=[ft.dropdown.Option(mes) for mes in dias_por_mes.keys()],
        label="Mês",
        width=110,
        bgcolor=FG,
        color="white",
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color="white"),
        border_color="white",
        on_change=atualizar_dias
    )

    dropdown_dia = ft.Dropdown(
        options=[],
        width=110,
        label="Dia",
        bgcolor=FG,
        color="white",
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color="white"),
        border_color="white",
    )

    circulo = ft.Stack(
        controls=[
            ft.Container(
                width=100,
                height=100,
                border_radius=50,
                bgcolor="white12"
            ),
            ft.Container(
                gradient=ft.SweepGradient(
                    center=ft.alignment.center,
                    start_angle=0.0,
                    end_angle=3,
                    stops=[0.5, 0.5],
                    colors=["#00000000", "blue"],
                ),
                width=100,
                height=100,
                border_radius=50,
                content=ft.Row(
                    alignment="center",
                    controls=[
                        ft.Container(
                            padding=ft.padding.all(5),
                            bgcolor=BG,
                            width=90,
                            height=90,
                            border_radius=50,
                            content=ft.Container(
                                bgcolor=FG,
                                height=80,
                                width=80,
                                border_radius=40,
                                content=ft.Image(
                                    src="fotopet.jpeg",
                                    width=80,
                                    height=80,
                                    fit=ft.ImageFit.COVER
                                )
                            )
                        )
                    ]
                )
            )
        ]
    )

    conteudo_primeira_pagina = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Container(on_click=lambda e: abrir_menu(e),
                                     bgcolor="white",
                                     content=ft.Icon(ft.Icons.MENU)
                                     )
                    ]
                ),
                ft.Text(value="Olá Brandon!", font_family="Arial",
                        size=30, color="white"),
                ft.Text(value="PET BELIZE", font_family="Arial",
                        size=15, color="white"),
                nome_cliente_text,
                nome_cliente_input,
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Column(
                            controls=[
                                celular_text,
                                celular_input
                            ]
                        ),
                    ]
                ),
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Column(controls=[data_text, data_input]),
                        ft.Column(controls=[horario_text, horario_input])
                    ]
                ),
                ft.Row(
                    alignment="spaceBetween",
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(controls=[nome_pet_text, nome_pet_input]),
                        ft.Column(controls=[sexo_text, sexo_dropdown])
                    ]
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=servicos_text,
                                bgcolor=AZUL_CLARO,
                                padding=ft.padding.symmetric(
                                    horizontal=15, vertical=5),
                                border_radius=10
                            ),
                            ft.Row(
                                controls=[servicos_dropdown,
                                          servicos_textfield]
                            )
                        ]
                    )
                ),
                observacoes_text,
                observacoes_input,
                ft.Row(
                    controls=[pagamento_dropdown, dinheiro_input],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Row(
                    controls=[cadastrar_botao],
                    alignment=ft.MainAxisAlignment.END
                )
            ]
        )
    )

    conteudo_segunda_pagina = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Container(
                            on_click=lambda e: abrir_menu_secundario(e),
                            bgcolor="white",
                            content=ft.Icon(ft.Icons.MENU)
                        )
                    ]
                ),
                ft.Container(height=30),
                ft.Row(
                    alignment="left",
                    controls=[
                        ft.Container(
                            ft.Text("Gerenciamento de Entrada/Saída",
                                    font_family="arial", size=24, color="white")
                        )
                    ]
                ),
                ft.Container(height=20),
                ft.Row(
                    alignment="left",
                    controls=[filtrar_dados]
                ),
                ft.Row(
                    alignment="center",
                    controls=[dropdown_mes, dropdown_dia, dropdown_ano]
                ),
                ft.Container(height=20),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                data_table
                            ],
                            scroll="auto"
                        )
                    ],
                    height=400,
                    scroll="auto"
                ),
                ft.Row(
                    alignment="end",
                    controls=[botao_saida]
                )
            ]
        )
    )

    menu_lateral = ft.Container(
        width=400,
        height=850,
        bgcolor=BG,
        border_radius=35,
        padding=ft.padding.only(left=50, top=60, right=200),
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment="left",
                    controls=[
                        ft.Container(border_radius=25,
                                     padding=ft.padding.only(
                                         top=13, left=13),
                                     height=50,
                                     width=50,
                                     border=ft.border.all(
                                         color="white", width=1),
                                     on_click=lambda e: (restore_menu(
                                         e), restore_menu_secundario(e)),
                                     content=ft.Text("<", color="black")
                                     )
                    ]
                ),
                ft.Container(height=20),
                circulo,
                ft.Text("Brandon\nViana", size=32,
                        color="white"
                        ),
                ft.Container(height=25),
                ft.Row(
                    alignment="left",
                    controls=[
                        ft.Container(
                            on_click=pagina_principal_view,
                            content=ft.Text(
                                "Página Principal", size=20, color="white"
                            )
                        )
                    ]
                ),
                ft.Row(
                    alignment="left",
                    controls=[
                        ft.Container(
                            on_click=pagina_historico,
                            content=ft.Text(
                                "Histórico", size=20, color="white")
                        )
                    ]
                )
            ]
        )
    )

    pagina_principal = ft.Row(alignment="end",
                              controls=[
                                  ft.Container(
                                      width=400,
                                      height=850,
                                      bgcolor=FG,
                                      border_radius=35,
                                      animate=ft.animation.Animation(
                                        600, ft.AnimationCurve.DECELERATE),
                                      animate_scale=ft.animation.Animation(
                                          400, curve="decelerate"),
                                      padding=ft.padding.only(
                                          top=50, left=20,
                                          right=20, bottom=5
                                      ),
                                      content=ft.Column(
                                          controls=[
                                              conteudo_primeira_pagina
                                          ]
                                      )
                                  )
                              ],
                              opacity=1.0
                              )

    pagina_secundaria = ft.Row(
        alignment="end",
        visible=False,
        controls=[
            ft.Container(
                width=400,
                height=850,
                bgcolor=FG,
                border_radius=35,
                animate=ft.animation.Animation(
                    600, ft.AnimationCurve.DECELERATE),
                animate_scale=ft.animation.Animation(400, curve="decelerate"),
                padding=ft.padding.only(top=50, left=20, right=20, bottom=5),
                content=ft.Column(
                    controls=[
                        conteudo_segunda_pagina
                    ]
                )
            )
        ]
    )

    background = ft.Container(
        width=400,
        height=850,
        bgcolor=BG,
        border_radius=35,
        content=ft.Stack(
            controls=[
                menu_lateral,
                pagina_secundaria,
                pagina_principal,

            ]
        )

    )

    page.add(
        background
    )


ft.app(target=main)
