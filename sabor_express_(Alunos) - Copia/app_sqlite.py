# Importação de bibliotecas necessárias
import os
import sqlite3

def inicializar_banco():
    """
    Função para inicializar o bando de dados SQLite
    Cria a tabela restaurantes se ela não existir
    """
    conn = sqlite3.connect('restaurantes.db')
    cursor = conn.cursor()

    # Criar tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # Inserir dados iniciais apenas se a tabela estiver vazia
    cursor.execute('SELECT COUNT(*) FROM restaurantes')
    count = cursor.fetchone()[0]

    if count == 0:
        restaurantes_iniciais = [
            ('Praça', 'Japonesa', False),
            ('Pizza Suprema', 'Pizza', True),
            ('Cantina', "Italiano", False)
        ]

        cursor.executemany('''
                INSERT INTO restaurantes (nome, categoria, ativo) VALUES (?, ?, ?)
        ''', restaurantes_iniciais) 

    conn.commit()
    conn.close()

def exibir_nome_do_programa():
    """
    Função para exibir o nome do programa de forma estilizada
    """ 
    print("""
    𝕊𝕒𝕓𝕠𝕣 𝕖𝕩𝕡𝕣𝕖𝕤𝕤
    """)

def exibir_opcoes():
    print('1. Cadastrar restaurante')
    print('2. Listar restaurante')
    print('3. Alternar estado do restaurante')
    print('4. Excluir restaurante')
    print('5. Sair\n')

def finalizar_app():
    """
    Função para finalizar o aplicativo
    """
    exibir_subtitulo('Finalizando o app\n')

def voltar_ao_menu_principal():
    """
    Função para retornar ao menu principal após uma operação
    """
    input('\nDigite uma tecla para voltar ao menu principal')
    main()

def opcao_invalida():
    """
    Função para tratar opções inválidas inseridas pelo usuário
    """
    print('Opção inválida!\n')
    voltar_ao_menu_principal()

def exibir_subtitulo(texto):
    """
    Função para exibir um subtítulo formatado
    :param texto: Texto do subtítulo
    """
    os.system('cls') #Limpa a tela (funciona apenas no Windows)
    linha = '*' * (len(texto))
    print(linha)
    print(texto)
    print(linha)
    print()

def cadastrar_novo_restaurante():
    """
    Função para cadastrar um novo restaurante
    
    Inputs:
    - Nome do restaurante
    - Categoria

    Outputs:
    - Adiciona um novo restaurante à lista de restaurantes
    """
    exibir_subtitulo('Cadastro de novos restaurantes\n')
    nome_do_restaurante = input('Digite o nome do restaurante que deseja cadastrar: ')
    categoria = input(f'Digite o nome da categoria do restaurante {nome_do_restaurante}: ')

    try:
        conn = sqlite3.connect('restaurantes.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO restaurantes (nome, categoria, ativo) VALUES (?, ?, ?)
        ''', (nome_do_restaurante, categoria, False))

        conn.commit()
        conn.close()

        print(f'O restaurante {nome_do_restaurante} foi cadastrado com sucesso')

    except sqlite3.Error as e:
        print(f'Erro ao cadastrar restaurante: {e}')

    voltar_ao_menu_principal()

def alternar_estado_do_restaurante():
    """
    Função para ativar ou desativar um restaurante
    """
    exibir_subtitulo('Alternando estado do restaurante\n')
    nome_restaurante = input('Digite o nome do restaurante que deseja alterar o estado: ')

    try:
        conn = sqlite3.connect('restaurantes.db')
        cursor = conn.cursor()

        # Verificar se o restaurante existe e buscar seu estado atual
        cursor.execute('SELECT ativo FROM restaurante WHERE nome = ?', (nome_restaurante,))
        resultado = cursor.fetchone()

        if resultado is not None:
            estado_atual = resultado[0]
            novo_estado = not estado_atual

            # Atualizar o estado
            cursor.execute('''
                UPDATE restaurantes SET ativo = ? WHERE nome = ?
            ''', (novo_estado, nome_restaurante))

            conn.commit()

            mensagem = f'O restaurante {nome_restaurante} foi ativado com sucesso!' if novo_estado else f'O restaurante {nome_restaurante} foi desativada com sucesso!'
            print(mensagem)
        else:
            print('O restaurante não foi encontrado!')
        
        conn.close()

    except sqlite3.Error as e:
        print(f'Erro ao alterar estado do restaurante: {e}')

    voltar_ao_menu_principal() 

def excluir_restaurante():
    """
    Função para excluir um restaurante do banco de dados
    """
    exibir_subtitulo('Excluir restaurante\n')

    # Primeiro, listar os restaurantes disponíveis
    try:
        conn = sqlite3.connect('restaurantes.db')
        cursor = conn.cursor()

        cursor.execute('SELECT nome, categoria FROM restaurantes ORDER BY nome')
        restaurantes = cursor.fetchall()

        if restaurantes:
            print('Restaurantes cadastrados')
            print('-' * 40)
            for restaurante in restaurantes:
                print(f'• {restaurante[0]} ({restaurante[1]})')
            print()

            nome_restaurante = input('Digite o nome do restaurante que deseja excluir: ')

            # Verificar se o restaurante existe
            cursor.execute('SELECT id FROM restaurantes WHERE nome = ?', (nome_restaurante,))
            resultado = cursor.fetchone()

            if resultado is not None:
                confirmacao = input (f'Tem certeza que deseja excluir o restaurante "{nome_restaurante}"? (s/n): ')

                if confirmacao.lower() == 's':
                    cursor.execute('DELETE FROM restaurante WHERE nome = ?', (nome_restaurante,))
                    conn.commit()
                    print(f'O restaurante {nome_restaurante} foi excluído com sucesso!')
                else:
                    print('Exclusão cancelada.')
            else:
                print('O restaurante não foi encontrado!')
        else:
            print('Nenhuma restaurante cadastrado para excluir.')

        conn.close()
    
    except sqlite3.Error as e:
        print(f'Erro ao excluir restaurante: {e}')

    voltar_ao_menu_principal()

def listar_restaurantes():
    """
    Função para listar todos os restaurantes cadastrados
    """
    exibir_subtitulo('Listando os restaurantes\n')

    try: 
        conn = sqlite3.connect('restaurantes.db')
        cursor = conn.cursor()

        cursor.execute('SELECT nome, categoria, ativo FROM restaurantes ORDER BY nome')
        restaurantes = cursor.fetchall()

        if restaurantes:
            print(f'{'Nome do Restaurante'.ljust(21)} | {'Categoria'.ljust(20)} | Status')
            print('-' * 65)

            for restaurante in restaurantes:
                nome = restaurante[0]
                categoria = restaurante[1]
                ativo = 'ativado' if restaurantes[2] else 'desativado'
                print(f'{nome.ljust(21)} | {categoria.ljust(20)} | {ativo}')
            else:
                print('Nenhum restaurante cadastrado.')

            conn.close()

    except sqlite3.Error as e:
        print(f'Erro ao listar restaurantes: {e}')  

    voltar_ao_menu_principal()

def escolher_opcao():
    """
    Função para processar a escolha do usuário no menu principal
    """
    try:
        opcao_escolhida = int(input('Escolha uma opção: '))

        if opcao_escolhida == 1:
            cadastrar_novo_restaurante()
        elif opcao_escolhida == 2:
            listar_restaurantes()
        elif opcao_escolhida == 3:
            alternar_estado_do_restaurante()
        elif opcao_escolhida == 4:
            excluir_restaurante()
        elif opcao_escolhida == 5:
            finalizar_app()
        else:
            opcao_invalida()
    except:
        opcao_invalida()

# Quinta digitação
def main():
    """
    Função principal que inicia o programa
    """
    os.system('cls') # Limpa a tela (funciona apenas o windows)
    exibir_nome_do_programa()
    exibir_opcoes()
    escolher_opcao()

if __name__ == '__main__':
    main()


