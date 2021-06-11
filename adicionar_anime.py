from PyQt5 import uic, QtWidgets
import sqlite3

banco = sqlite3.connect('add_anime.db')
cursor = banco.cursor()
cursor.execute('CREATE TABLE if NOT EXISTS usuario(id integer primary key, nome text, login text, senha text)')
cursor.execute('CREATE TABLE IF NOT EXISTS animes(id integer primary key, nome text, ep integer, estado text)')


def adicionar_anime():
    nome = add_anime.input_nome.text()
    print('Anime: ', nome)
    ep = add_anime.input_ep.text()
    print('Nº Eps: ', ep)

    estado = ''
    if add_anime.radio_completo.isChecked():
        print('Estado: Completo')
        estado = 'Completo'
    elif add_anime.radio_incompleto.isChecked():
        print('Estado: Incompleto')
        estado = 'Incompleto'

    banco = sqlite3.connect('add_anime.db')
    cursor = banco.cursor()
    cursor.execute('INSERT INTO animes VALUES(null,"'+nome+'", "'+ep+'", "'+estado+'")')
    banco.commit()
    banco.close()
    add_anime.input_nome.setText('')
    add_anime.input_ep.setText('')
    add_anime.label_5.setText('Anime adicionado com sucesso')


def abrir_lista():
    tela_listaAnime.show()
    banco = sqlite3.connect('add_anime.db')
    cursor = banco.cursor()
    # comando SQL
    cursor.execute('SELECT * FROM animes')
    dados_lidos = cursor.fetchall()

    tela_listaAnime.table_list.setRowCount(len(dados_lidos))
    tela_listaAnime.table_list.setColumnCount(4)

    for linha in range(0, len(dados_lidos)):
        for coluna in range(4):
            tela_listaAnime.table_list.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))
    banco.close()


def excluir_item():
    linha = tela_listaAnime.table_list.currentRow()
    tela_listaAnime.table_list.removeRow(linha)
    banco = sqlite3.connect('add_anime.db')
    cursor = banco.cursor()
    cursor.execute('SELECT id FROM animes')
    dados_lidos = cursor.fetchall()
    dados_id = str(dados_lidos[linha][0])

    cursor.execute('DELETE FROM animes where id = "'+dados_id+'"')
    banco.commit()
    tela_listaAnime.close()
    abrir_lista()


def editar_anime():
    global linha_id
    menu_editar.show()
    linha = tela_listaAnime.table_list.currentRow()
    banco = sqlite3.connect('add_anime.db')
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM animes')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    linha_id = valor_id
    menu_editar.lineEdit.setText(str(dados_lidos[linha][0]))
    menu_editar.lineEdit_2.setText(str(dados_lidos[linha][1]))
    menu_editar.lineEdit_3.setText(str(dados_lidos[linha][2]))
    menu_editar.lineEdit_4.setText(str(dados_lidos[linha][3]))


def salvar_editado():
    global  linha_id
    nome = menu_editar.lineEdit_2.text()
    ep = menu_editar.lineEdit_3.text()
    estado = menu_editar.lineEdit_4.text()
    banco = sqlite3.connect('add_anime.db')
    cursor = banco.cursor()
    cursor.execute('UPDATE animes SET nome = "'+nome+'", ep ="'+str(ep)+'", estado = "'+estado+'" WHERE id = "'+str(linha_id)+'"')
    banco.commit()
    menu_editar.close()
    abrir_lista()


# SISTEMA DE LOGIN
def efetuar_login():
    nome_usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()
    tela_login.label_4.setText('')
    try:
        banco = sqlite3.connect('add_anime.db')
        cursor = banco.cursor()
        cursor.execute('SELECT senha FROM usuario WHERE login = "'+nome_usuario+'"')
        senha_bd = cursor.fetchall()

        if senha == senha_bd[0][0]:
            tela_login.lineEdit.setText('')
            tela_login.close()
            add_anime.show()
        else:
            tela_login.label_4.setText('Usuario ou Senha invalido')
    except:
        tela_login.label_4.setText('Usuario Inexistente')

    tela_login.lineEdit_2.setText('')


def tela_cadastro():
    tela_cadastrar_conta.show()


def criar_usuario():
    nome = tela_cadastrar_conta.lineEdit.text()
    login = tela_cadastrar_conta.lineEdit_2.text()
    senha = tela_cadastrar_conta.lineEdit_3.text()
    c_senha = tela_cadastrar_conta.lineEdit_4.text()

    if(senha == c_senha):
        try:
            banco = sqlite3.connect('add_anime.db')
            cursor = banco.cursor()
            cursor.execute('INSERT INTO usuario VALUES(null, "'+nome+'", "'+login+'", "'+senha+'")')

            banco.commit()
            tela_login.label_4.setText('Usuario cadastrado com sucesso')
            tela_cadastrar_conta.close()

        except sqlite3.Error as erro:
            print('Erro ao inserir os dados: ', erro)
    else:
        tela_cadastrar_conta.label_2.setText('As senhas não correspondem')


def logout():
    add_anime.close()
    tela_login.show()


app = QtWidgets.QApplication([])
add_anime = uic.loadUi('adicionar_anime.ui')
add_anime.button_add.clicked.connect(adicionar_anime)
add_anime.button_list.clicked.connect(abrir_lista)
tela_listaAnime = uic.loadUi('myAnimeList.ui')
tela_listaAnime.button_excluir.clicked.connect(excluir_item)
tela_listaAnime.button_editar.clicked.connect(editar_anime)
menu_editar = uic.loadUi('menu_editar.ui')
menu_editar.pushButton.clicked.connect(salvar_editado)

tela_login = uic.loadUi('tela_login.ui')
tela_login.pushButton.clicked.connect(efetuar_login)
tela_login.lineEdit.returnPressed.connect(efetuar_login)
tela_login.lineEdit_2.returnPressed.connect(efetuar_login)

add_anime.pushButton.clicked.connect(logout)
tela_cadastrar_conta = uic.loadUi('cadastrar_usuario.ui')
tela_login.button_cadastrar.clicked.connect(tela_cadastro)
tela_cadastrar_conta.button_criar_conta.clicked.connect(criar_usuario)



tela_login.show()

app.exec()
