import ttkbootstrap as ttk  # Biblioteca para interfaces gráficas modernas com temas
from ttkbootstrap.constants import *  # Constantes de cores e estilos do ttkbootstrap
from PIL import Image, ImageTk  # Biblioteca PIL para manipulação de imagens
from functools import partial  # Permite criar funções com argumentos pré-definidos
import os  # Biblioteca para manipulação de arquivos e caminhos
import sys  # Biblioteca para variáveis e funções do sistema

def resource_path(relative_path):
    """
    Obtém o caminho absoluto de um recurso (imagem, ícone etc.),
    funcionando tanto no desenvolvimento quanto quando empacotado com PyInstaller.
    """
    try:
        base_path = sys._MEIPASS  # Caminho temporário do PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # Caminho local da aplicação
    return os.path.join(base_path, relative_path)


class Calculadora:
    def __init__(self):
        # Inicializa a janela principal com título e tema
        self.janela = ttk.Window(title="Calculadora SENAI", themename="darkly")
        self.janela.geometry('400x750')  # Define tamanho da janela

        # Configurações de cores e fontes
        self.cor_fundo = 'black'
        self.cor_botao = 'secondary'
        self.cor_texto = 'white'
        self.cor_operacao = 'warning'
        self.font_botao = ('Roboto', 18)
        self.font_display = ('Roboto', 36)

        # Configura o ícone da janela (se existir)
        icon_path = resource_path('calc.ico')
        if os.path.exists(icon_path):
            self.janela.iconbitmap(icon_path)

        # Frame para o display da calculadora
        self.display_frame = ttk.Frame(self.janela)
        self.display_frame.pack(fill='both', expand=True)

        # Label que mostra os números e resultados
        self.display = ttk.Label(
            self.display_frame,
            text='',
            font=self.font_display,
            anchor='e',  # Alinha o texto à direita
            padding=(20, 10)
        )
        self.display.pack(fill='both', expand=True)

        # Frame que vai conter todos os botões
        self.buttons_frame = ttk.Frame(self.janela)
        self.buttons_frame.pack(fill='both', expand=True)

        # Lista de botões da calculadora
        self.botoes = [
            ['C', '⌫', '^', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', '-'],
            ['.', '0', '()', '=']
        ]

        # Criação dos botões dinamicamente
        for i, linha in enumerate(self.botoes):
            for j, texto in enumerate(linha):
                # Define o estilo do botão (operadores em destaque)
                estilo = 'warning.TButton' if texto in ['C', '⌫', '^', '/', 'x', '+', '-', '='] else 'secondary.TButton'
                botao = ttk.Button(
                    self.buttons_frame,
                    text=texto,
                    style=estilo,
                    width=10,
                    command=partial(self.interpretar_botao, texto)  # Liga o botão à função interpretar_botao
                )
                botao.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')  # Posiciona o botão no grid

        # Configura o grid para que os botões se expandam proporcionalmente
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.buttons_frame.grid_columnconfigure(j, weight=1)

        # Frame para exibir a imagem do SENAI
        self.frame_imagem = ttk.Frame(self.janela)
        self.frame_imagem.pack(fill='both', expand=True)

        imagem_path = resource_path('Senai.png')
        if os.path.exists(imagem_path):
            imagem = Image.open(imagem_path)
            imagem = imagem.resize((300, 100), Image.LANCZOS)  # Redimensiona a imagem
            imagem_tk = ImageTk.PhotoImage(imagem)
            label_imagem = ttk.Label(self.frame_imagem, image=imagem_tk, text="")
            label_imagem.image = imagem_tk  # Mantém referência para não sumir
            label_imagem.pack()

        # Frame para seletor de temas
        self.frame_tema = ttk.Frame(self.janela)
        self.frame_tema.pack(fill='x', padx=10, pady=10)

        # Label informativa do seletor
        self.label_tema = ttk.Label(self.frame_tema, text="Escolher tema:", font=('Roboto', 12))
        self.label_tema.pack(side='top', pady=(0, 5))

        # Combobox com lista de temas disponíveis
        self.temas = ['darkly', 'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse',
                      'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerulean']
        self.selector_tema = ttk.Combobox(self.frame_tema, values=self.temas, state='readonly')
        self.selector_tema.set('darkly')  # Tema inicial
        self.selector_tema.pack(side='top', fill='x')
        self.selector_tema.bind("<<ComboboxSelected>>", self.mudar_tema)  # Evento para mudar tema

        # Inicia a interface
        self.janela.mainloop()

    def mudar_tema(self, evento):
        """
        Altera o tema da calculadora quando um novo tema é selecionado no combobox.
        """
        novo_tema = self.selector_tema.get()
        self.janela.style.theme_use(novo_tema)

    def interpretar_botao(self, valor):
        """
        Função que interpreta o valor do botão pressionado.
        """
        texto_atual = self.display.cget("text")

        if valor == 'C':  # Limpar display
            self.display.configure(text='')
        elif valor == '⌫':  # Apagar último caractere
            self.display.configure(text=texto_atual[:-1])
        elif valor == '=':  # Calcular expressão
            self.calcular()
        elif valor == '()':  # Adicionar parênteses
            if not texto_atual or texto_atual[-1] in '+-/*':
                self.display.configure(text=texto_atual + '(')
            elif texto_atual[-1].isdigit():
                self.display.configure(text=texto_atual + ')')
        else:  # Adicionar números ou operadores
            self.display.configure(text=texto_atual + valor)

    def calcular(self):
        """
        Avalia a expressão matemática no display e exibe o resultado.
        """
        # Substitui operadores para sintaxe do Python
        expressao = self.display.cget("text").replace('x', '*').replace('^', '**')
        try:
            resultado = eval(expressao)  # Avalia a expressão
            self.display.configure(text=str(resultado))
        except:
            self.display.configure(text='Erro')  # Mostra erro se a expressão for inválida


# Executa a calculadora
if __name__ == "__main__":
    Calculadora()