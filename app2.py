import flet as ft
from flet import AppBar, Text, View, ElevatedButton
from flet.core.colors import Colors
from sqlalchemy import select
from models import *


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    funcionarios = []

    def salvar_funcionario(e):
        if input_nome.value == "" or input_nome.value == "" or input_cargo.value == "" or input_salario.value == "":
            page.overlay.append(msg_erro)
            msg_erro.open = True
            page.update()
        else:
            funcionario = Funcionario(
                nome=input_nome.value,
                cargo=input_cargo.value,
                salario=input_salario.value,
            )
            funcionario.save()
            input_nome.value = ""
            input_cargo.value = ""
            input_salario.value = ""
            msg_sucesso.open = True
            page.update()

    def exibir_lista(e):
        lv_funci.controls.clear()

        pessoa = select(Funcionario)
        funcionarios = db_session.execute(pessoa).scalars().all()

        for l in funcionarios:
            lv_funci.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(l.nome),
                    subtitle=ft.Text(l.cargo),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Detalhes do Funcionario"
                            ),
                        ],
                        on_select=lambda _, liv=l: ver_detalhes(liv.nome, liv.cargo, liv.salario),
                    )

                )
            )
        page.update()

    def ver_detalhes(nome, cargo, salario):
        txt.value = f"Nome: {nome}; \nCargo: {cargo}; \nSalario: {salario}."
        page.go("/listar_detalhes")

    def gerencia_rota(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Cadastro de Funcionario"), bgcolor=Colors.BLUE_900),
                    input_nome,
                    input_cargo,
                    input_salario,
                    ElevatedButton(text="Salvar Funcionario", on_click=salvar_funcionario, color=ft.CupertinoColors.SYSTEM_BLUE, width=375),
                    ElevatedButton(text="Exibir Lista de funcionario", on_click=lambda _: page.go("/lista"), color=ft.CupertinoColors.SYSTEM_BLUE, width=375),
                ]
            )
        )
        if page.route == "/lista":
            exibir_lista(e)
            page.views.append(
                View(
                    "/lista",
                    [
                        AppBar(title=Text("Lista de Funcionario"), bgcolor=Colors.BLUE_900),
                        lv_funci
                    ]
                )
            )

        if page.route == "/listar_detalhes":
            page.views.append(
                View(
                    "/listar_detalhes",
                    [
                        AppBar(title=Text("Lista de Funcionario"), bgcolor=Colors.BLUE_900),
                        txt,
                        ElevatedButton(text="Voltar", on_click=lambda _: page.go("/lista"), color=ft.CupertinoColors.SYSTEM_BLUE, width=375)
                    ]
                )
            )
        page.update()

    # Campos
    input_nome = ft.TextField(label="Nome")
    input_cargo = ft.TextField(label="Cargo")
    input_salario = ft.TextField(label="Salario")
    txt = ft.Text(value="")

    lv_funci = ft.ListView(
        height=500,
        spacing=1,
        divider_thickness=1,
    )

    msg_sucesso = ft.SnackBar(content=Text("Funcionario cadastrado!"), bgcolor=Colors.GREEN)
    msg_erro = ft.SnackBar(content=Text("Não deixe campos vazio!"), bgcolor=Colors.RED)

    page.overlay.append(msg_sucesso)
    page.overlay.append(msg_erro)

    page.on_route_change = gerencia_rota

    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)