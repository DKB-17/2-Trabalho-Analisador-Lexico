import sys 
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import re
import io
from contextlib import redirect_stdout

# =========================================================
# 1. CLASSE DO ANALISADOR LÉXICO 
# =========================================================
class LexerSertaLanguage:
    def __init__(self):
        
        self.palavras_reservadas = {
            'Receita', 'receita', 'Trem', 'trem', 'Bisbilhota', 'bisbilhota','fala_tu', 'Fala_tu', 
            'meteope', 'Meteope', 'Sepa', 'sepa','hum', 'Hum', 'vixe', 'Vixe', 'Vorta', 'vorta'
        }
        
        # Tipos de Dados da linguagem
        self.tipos_dados = {
            'Cheio', 'cheio', 'Quebrado', 'Prosa', 'Confuso', 'Domino', 'Oco', 'Bagulho'
        }
        
        # Operadores Lógicos
        self.operadores_logicos = {'I', 'U', 'Nem_a_pau'}

        # Regras Regex
        self.regras_tokens = [
            ('ESCOPO', r'\{\[|\]\}'),               
            ('TERMINAL', r'[Uu]ai'),             
            ('OP_RELACIONAL', r'<=|>=|==|<|>'),     
            ('OP_ATRIBUICAO', r'='),                
            ('OP_ARITMETICO', r'[+\-*/]'),          
            ('CARACTERE_ESP', r'[(),]'),            
            ('NUMERAL', r'\d+'),                    
            ('PALAVRA', r'[A-Za-z_][A-Za-z0-9_]*'), 
            ('ESPACO', r'[ \t]+'),                  
            ('DESCONHECIDO', r'.')                  
        ]
        
        self.regex_mestre = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in self.regras_tokens)

    def analisar(self, codigo_fonte):
        """Faz a análise léxica e imprime no console."""
        linhas = codigo_fonte.split('\n')
        total_linhas = len(linhas)
        erros = 0

        lista_tokens = []
        
        print("\n" + "="*50)
        print("I) RESULTADO GERADO PELO ANALISADOR LEXICO")
        print("="*50 + "\n")
        
        for numero_linha, linha in enumerate(linhas):
            if not linha.strip():
                print(f"Linha {numero_linha}: do Programa, contém as seguintes Informações: (Linha em branco)")
                continue
                
            resultado_linha = f"Linha {numero_linha}: do Programa, contém as seguintes Informações:"
            
            for match in re.finditer(self.regex_mestre, linha):
                tipo_regex = match.lastgroup 
                valor = match.group()        
                
                if tipo_regex == 'ESPACO':
                    continue
                
                tipo_final = ""
                
                if tipo_regex == 'PALAVRA':
                    
                    if valor in self.palavras_reservadas:
                        tipo_final = "Palavra Reservada"
                    elif valor in self.tipos_dados:
                        tipo_final = "Tipo de Dados"
                    elif valor in self.operadores_logicos:
                        tipo_final = "Operador Lógico"
                    else:
                        tipo_final = "Variável" 
                
                elif tipo_regex == 'NUMERAL':
                    tipo_final = "Numeral"
                elif tipo_regex == 'OP_ATRIBUICAO':
                    tipo_final = "Operador de Atribuição"
                elif tipo_regex == 'OP_ARITMETICO':
                    tipo_final = "Operador Aritmético"
                elif tipo_regex == 'OP_RELACIONAL':
                    tipo_final = "Operador Relacional"
                elif tipo_regex == 'OP_LOGICO':
                    tipo_final = "Operador Lógico"
                elif tipo_regex == 'ESCOPO':
                    tipo_final = "Escopo"
                elif tipo_regex == 'TERMINAL':
                    tipo_final = "Terminal"
                elif tipo_regex == 'CARACTERE_ESP':
                    tipo_final = "Caractere Especial"
                elif tipo_regex == 'DESCONHECIDO':
                    tipo_final = "ERRO LÉXICO"
                    erros += 1

                resultado_linha += f"Token: {valor} -> {tipo_final}."

                print(f"Linha {numero_linha} | Token: {valor} -> {tipo_final}")
                
                lista_tokens.append({
                    'valor': valor,
                    'tipo': tipo_final,
                    'linha': numero_linha
                })
    
        print(f"\nAnálise Léxica Concluída! Total de Linhas: {total_linhas}, Erros Léxicos: {erros}.")
        return lista_tokens     
       


# =========================================================
# 3. CLASSE DA INTERFACE (A Mini-IDE)
# =========================================================
class Interface:
    def __init__(self, janela_principal):
        self.janela = janela_principal
        self.janela.title("SertaLanguage IDE - Analisador")
        self.janela.geometry("1000x600")
        self.lexer = LexerSertaLanguage()
        self.caminho_selecionado = ""

        # --- 1. PAINEL SUPERIOR (Botões de Ação) ---
        frame_top = tk.Frame(self.janela)
        frame_top.pack(fill=tk.X, padx=10, pady=10)

        self.botao_selecionar = tk.Button(
            frame_top,
            text="📂 1. Escolher Arquivo",
            command=self.escolher_arquivo
        )
        self.botao_selecionar.pack(side=tk.LEFT, padx=5)

        self.botao_enviar = tk.Button(
            frame_top,
            text="🚀 2. Analisar Código",
            command=self.enviar_arquivo
        )
        self.botao_enviar.pack(side=tk.LEFT, padx=5)

        self.label_info = tk.Label(
            frame_top,
            text="Nenhum arquivo selecionado."
        )
        self.label_info.pack(side=tk.LEFT, padx=15)

        # --- 2. PAINEL CENTRAL ---
        frame_meio = tk.PanedWindow(self.janela, orient=tk.HORIZONTAL)
        frame_meio.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame_codigo = tk.LabelFrame(frame_meio, text="Código Fonte (.txt)")
        self.area_codigo = scrolledtext.ScrolledText(
            frame_codigo,
            width=40,
            font=("Courier", 10)
        )
        self.area_codigo.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame_meio.add(frame_codigo)

        # --- 3. PAINEL DE SAÍDA COM ABAS ---
        frame_saida = tk.LabelFrame(
            frame_meio,
            text="Console de Compilação"
        )
        frame_saida.pack_propagate(False)

        self.abas_saida = ttk.Notebook(frame_saida)
        self.abas_saida.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Aba da análise léxica
        aba_lexica = tk.Frame(self.abas_saida, bg="#1E1E1E")
        self.area_lexica = scrolledtext.ScrolledText(
            aba_lexica,
            font=("Consolas", 10),
            bg="#1E1E1E",
            fg="#00FF00",
            insertbackground="white"
        )
        self.area_lexica.pack(fill=tk.BOTH, expand=True)
        self.abas_saida.add(aba_lexica, text="🔤 Análise Léxica")

        # Aba da análise sintática
        aba_sintatica = tk.Frame(self.abas_saida, bg="#1E1E1E")
        self.area_sintatica = scrolledtext.ScrolledText(
            aba_sintatica,
            font=("Consolas", 10),
            bg="#1E1E1E",
            fg="#00FF00",
            insertbackground="white"
        )
        self.area_sintatica.pack(fill=tk.BOTH, expand=True)
        self.abas_saida.add(aba_sintatica, text="🧩 Análise Sintática")

        frame_meio.add(frame_saida)

        # Configuração visual das mensagens.
        for widget in (self.area_lexica, self.area_sintatica):
            widget.tag_config("verde", foreground="#00FF00")
            widget.tag_config("vermelho", foreground="#FF5555")
            widget.tag_config("amarelo", foreground="#FFD700")

    def _mostrar_saida(self, widget, texto):
        """Insere uma saída no console usando a mesma codificação visual."""
        widget.delete("1.0", tk.END)

        for trecho in texto.splitlines(True):
            if "ERRO" in trecho or "Erro" in trecho or "[ERRO]" in trecho:
                tag = "vermelho"
            elif (
                "RESULTADO" in trecho
                or "ANALISE" in trecho
                or "ANÁLISE" in trecho
                or "====" in trecho
                or "SUCESSO" in trecho
                or "Resumo" in trecho
            ):
                tag = "amarelo"
            else:
                tag = "verde"

            widget.insert(tk.END, trecho, tag)

        widget.see(tk.END)

    def escolher_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo SertaLanguage",
            filetypes=[
                ("Arquivos de Texto", "*.txt"),
                ("Todos os Arquivos", "*.*")
            ]
        )

        if caminho:
            self.caminho_selecionado = caminho
            nome_arquivo = caminho.replace("\\", "/").split("/")[-1]
            self.label_info.config(
                text=f"Arquivo selecionado: {nome_arquivo}"
            )

            try:
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    conteudo = arquivo.read()

                self.area_codigo.delete("1.0", tk.END)
                self.area_codigo.insert(tk.END, conteudo)
            except Exception as e:
                messagebox.showerror(
                    "Erro",
                    f"Erro ao ler arquivo: {e}"
                )

    def enviar_arquivo(self):
        conteudo_codigo = self.area_codigo.get("1.0", tk.END).strip()

        if conteudo_codigo == "":
            messagebox.showwarning(
                "Aviso",
                "O código fonte está vazio. "
                "Selecione um arquivo ou digite algo."
            )
            return

        # Limpa as duas abas antes de iniciar uma nova análise.
        self.area_lexica.delete("1.0", tk.END)
        self.area_sintatica.delete("1.0", tk.END)

        try:
            # Captura a saída de cada etapa separadamente.
            saida_lexica = io.StringIO()
            with redirect_stdout(saida_lexica):
                lista_de_tokens = self.lexer.analisar(conteudo_codigo)

            saida_sintatica = io.StringIO()
            with redirect_stdout(saida_sintatica):
                sintatico = AnalisadorSintatico(lista_de_tokens)
                sintatico.analisar()

            self._mostrar_saida(
                self.area_lexica,
                saida_lexica.getvalue()
            )
            self._mostrar_saida(
                self.area_sintatica,
                saida_sintatica.getvalue()
            )

            # Por padrão, mostra primeiro a análise léxica.
            self.abas_saida.select(0)

        except Exception as erro:
            mensagem = (
                "\nERRO FATAL NA COMPILAÇÃO:\n"
                f"{erro}\n"
            )
            self._mostrar_saida(self.area_sintatica, mensagem)
            self.abas_saida.select(1)


# =========================================================
# 2. CLASSE DO ANALISADOR SINTÁTICO (PARSER RECURSIVO)
# =========================================================
class AnalisadorSintatico:
    """
    Analisador sintático por descida recursiva para a SertaLanguage.

    Gramática implementada:
        programa      := Receita VAR '(' ')' '{[' comando* ']}' Uai?
        comando      := declaracao | atribuicao | fala | sepa | vorta
        declaracao   := Trem TIPO VAR (',' VAR)* TERMINAL
        atribuicao   := VAR '=' expressao TERMINAL
        fala          := Fala_tu '(' expressao ')' TERMINAL
        sepa         := Sepa '(' condicao ')' bloco TERMINAL
        vorta         := Vorta '(' condicao ')' bloco TERMINAL
        bloco        := '{[' comando* ']}'
        condicao     := expressao relacional expressao
                         (logico expressao relacional expressao)*
        expressao    := termo (('+' | '-') termo)*
        termo        := fator (('*' | '/') fator)*
        fator        := NUMERAL | VAR | '(' expressao ')'

    O Uai final do programa é opcional porque o arquivo de exemplo
    fornecido termina diretamente com ']}' após a estrutura principal.
    """

    RESERVADA = "Palavra Reservada"
    TIPO_DADO = "Tipo de Dados"
    VARIAVEL = "Variável"
    NUMERAL = "Numeral"
    ATRIBUICAO = "Operador de Atribuição"
    ARITMETICO = "Operador Aritmético"
    RELACIONAL = "Operador Relacional"
    CARACTERE = "Caractere Especial"
    ESCOPO = "Escopo"
    TERMINAL = "Terminal"

    LOGICOS = {"I", "U", "Nem_a_pau"}

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao_atual = 0
        self.erros = []
        self.erros_por_linha = {}

    def token_atual(self):
        if self.posicao_atual < len(self.tokens):
            return self.tokens[self.posicao_atual]
        return None

    def eh(self, tipo=None, valor=None):
        token = self.token_atual()
        if token is None:
            return False
        if tipo is not None and token["tipo"] != tipo:
            return False
        if valor is not None and token["valor"] != valor:
            return False
        return True

    def avancar(self):
        token = self.token_atual()
        if token is not None:
            self.posicao_atual += 1
        return token

    def registrar_erro(self, mensagem, token=None):
        token = token or self.token_atual()
        if token is None:
            linha = self.tokens[-1]['linha'] if self.tokens else 0
            texto = f"Erro sintatico: código terminou inesperadamente; {mensagem}."
            self.erros.append(texto)
            self.erros_por_linha.setdefault(linha, []).append(texto)
        else:
            linha = token['linha']
            texto = (
                f"Erro sintatico: encontrou '{token['valor']}', "
                f"{mensagem}."
            )
            self.erros.append(
                f"Erro Sintático na linha {linha}: {texto}"
            )
            self.erros_por_linha.setdefault(linha, []).append(texto)

    def consumir(self, tipo, valor=None, descricao=None):
        if self.eh(tipo, valor):
            return self.avancar()

        esperado = descricao or (f"'{valor}'" if valor is not None else tipo)
        token = self.token_atual()

        if token is None:
            self.registrar_erro(f"esperava {esperado}")
        else:
            # Se o próximo token já está em outra linha, o erro normalmente
            # é uma construção que ficou incompleta na linha anterior.
            linha_erro = token['linha']
            if self.posicao_atual > 0:
                anterior = self.tokens[self.posicao_atual - 1]
                if token['linha'] > anterior['linha']:
                    linha_erro = anterior['linha']

            token_erro = dict(token)
            token_erro['linha'] = linha_erro
            self.registrar_erro(
                f"esperava {esperado}, mas encontrou '{token['valor']}'"
                f" nesta posição",
                token_erro
            )
        return None

    def eh_reservada(self, *valores):
        token = self.token_atual()
        return (
            token is not None
            and token["tipo"] == self.RESERVADA
            and token["valor"] in valores
        )

    def eh_tipo_dado(self):
        token = self.token_atual()
        return token is not None and token["tipo"] == self.TIPO_DADO

    def eh_variavel(self):
        token = self.token_atual()
        return token is not None and token["tipo"] == self.VARIAVEL

    def eh_numero(self):
        token = self.token_atual()
        return token is not None and token["tipo"] == self.NUMERAL

    def eh_operador_relacional(self):
        token = self.token_atual()
        return token is not None and token["tipo"] == self.RELACIONAL

    def eh_operador_logico(self):
        token = self.token_atual()
        # O lexer classifica I/U/Nem_a_pau como "Variável" nesta versão.
        return (
            token is not None
            and token["tipo"] == self.VARIAVEL
            and token["valor"] in self.LOGICOS
        )

    def eh_operador_aritmetico(self, *operadores):
        token = self.token_atual()
        if token is None or token["tipo"] != self.ARITMETICO:
            return False
        return not operadores or token["valor"] in operadores

    def analisar(self):
        print("\n" + "=" * 50)
        print("II) RESULTADO GERADO PELO ANALISADOR SINTATICO")
        print("=" * 50 + "\n")

        # Registra erros léxicos como problemas da respectiva linha,
        # pois o sintático depende dos tokens produzidos pelo lexer.
        for token in self.tokens:
            if token["tipo"] == "ERRO LÉXICO":
                mensagem = (
                    f"Erro sintatico: token desconhecido '{token['valor']}'."
                )
                self.erros.append(
                    f"Erro Sintático na linha {token['linha']}: {mensagem}"
                )
                self.erros_por_linha.setdefault(token['linha'], []).append(mensagem)

        self.programa()

        if self.posicao_atual < len(self.tokens):
            while self.token_atual() is not None:
                token = self.avancar()
                self.registrar_erro(
                    f"o token '{token['valor']}' não pode aparecer neste ponto" ,
                    token
                )

        self.erros = list(dict.fromkeys(self.erros))

        # O relatório é deliberadamente simples: uma linha do relatório
        # para cada linha encontrada no código-fonte.
        total_linhas = max((token['linha'] for token in self.tokens), default=0) + 1

        for linha in range(total_linhas):
            erros = self.erros_por_linha.get(linha, [])
            if erros:
                # A Interface pinta automaticamente mensagens contendo "Erro" de vermelho.
                for erro in dict.fromkeys(erros):
                    print(f"Linha {linha}: {erro}")
            else:
                print(f"Linha {linha}: sem erros")

        print(
            f"\nAnálise Sintática Concluída! Total de Linhas: {total_linhas}, "
            f"Erros Sintáticos: {len(self.erros)}."
        )

        if not self.erros:
            print("[SUCESSO] NENHUM ERRO SINTATICO ENCONTRADO!")
            return True

        print("[ERRO] FORAM ENCONTRADOS ERROS SINTÁTICOS.")
        return False

    # ---------------------------------------------------------
    # programa := Receita VAR '(' ')' '{[' comando* ']}' Uai?
    # ---------------------------------------------------------
    def programa(self):
        sucesso = True

        if not (self.eh(self.RESERVADA, "Receita") or
                self.eh(self.RESERVADA, "receita")):
            self.registrar_erro("esperava a palavra reservada 'Receita'")
            sucesso = False
        else:
            self.avancar()

        if not self.consumir(self.VARIAVEL, descricao="o nome da receita"):
            sucesso = False

        if not self.consumir(self.CARACTERE, "(",
                             "o caractere '('"):
            sucesso = False

        if not self.consumir(self.CARACTERE, ")",
                             "o caractere ')'"):
            sucesso = False

        if not self.consumir(self.ESCOPO, "{[",
                             "a abertura de escopo '{['"):
            sucesso = False

        while (self.token_atual() is not None
               and not self.eh(self.ESCOPO, "]}")):
            if not self.comando():
                token = self.token_atual()
                if token is None:
                    break

                # Se a falha anterior deixou o parser exatamente no início
                # de uma nova linha que começa com uma variável, essa variável
                # pode ser um comando válido da próxima linha.
                if (token["tipo"] == self.VARIAVEL and
                        self.posicao_atual > 0 and
                        token["linha"] > self.tokens[self.posicao_atual - 1]["linha"]):
                    continue

                self.registrar_erro(
                    f"esperava um comando válido, mas encontrou "
                    f"'{token['valor']}'",
                    token
                )
                self.recuperar_comando()
                sucesso = False

        if not self.consumir(self.ESCOPO, "]}",
                             "o fechamento de escopo ']}'"):
            sucesso = False
            return sucesso

        # O exemplo fornecido termina em ]}. Para compatibilidade com
        # a versão anterior do código, também aceitamos Uai/uai aqui.
        if self.eh(self.TERMINAL):
            self.avancar()

        return sucesso

    # ---------------------------------------------------------
    # comando := declaracao | atribuicao | fala | sepa | vorta
    # ---------------------------------------------------------
    def comando(self):
        if self.eh_reservada("Trem", "trem"):
            return self.declaracao()

        if self.eh_reservada("Fala_tu", "fala_tu"):
            return self.fala()

        if self.eh_reservada("Sepa", "sepa"):
            return self.sepa()

        if self.eh_reservada("Vorta", "vorta"):
            return self.vorta()

        if self.eh_variavel():
            # I/U/Nem_a_pau são operadores lógicos, não comandos.
            if self.token_atual()["valor"] in self.LOGICOS:
                return False
            return self.atribuicao()

        return False

    # ---------------------------------------------------------
    # declaracao := Trem TIPO VAR (',' VAR)* TERMINAL
    # ---------------------------------------------------------
    def declaracao(self):
        self.avancar()

        if not self.eh_tipo_dado():
            self.registrar_erro("esperava um tipo de dado após 'Trem'")
            self.recuperar_comando()
            return False
        self.avancar()

        if not self.eh_variavel():
            self.registrar_erro("esperava uma variável na declaração")
            self.recuperar_comando()
            return False
        self.avancar()

        while self.eh(self.CARACTERE, ","):
            self.avancar()
            if not self.eh_variavel():
                self.registrar_erro("esperava uma variável após ','")
                self.recuperar_comando()
                return False
            self.avancar()

        return self.consumir(
            self.TERMINAL,
            descricao="o terminal 'Uai' ou 'uai' da declaração"
        ) is not None

    # ---------------------------------------------------------
    # atribuicao := VAR '=' expressao TERMINAL
    # ---------------------------------------------------------
    def atribuicao(self):
        self.avancar()

        if not self.consumir(
            self.ATRIBUICAO, "=", "o operador '='"
        ):
            self.recuperar_comando()
            return False

        if not self.expressao():
            self.registrar_erro("esperava uma expressão após '='")
            self.recuperar_comando()
            return False

        return self.consumir(
            self.TERMINAL,
            descricao="o terminal 'Uai' ou 'uai' da atribuição"
        ) is not None

    # ---------------------------------------------------------
    # fala := Fala_tu '(' expressao ')' TERMINAL
    # ---------------------------------------------------------
    def fala(self):
        self.avancar()

        if not self.consumir(
            self.CARACTERE, "(", "o caractere '('"
        ):
            return False

        if not self.expressao():
            self.registrar_erro(
                "esperava uma expressão dentro de 'Fala_tu(...)'"
            )
            self.recuperar_comando()
            return False

        if not self.consumir(
            self.CARACTERE, ")", "o caractere ')'"
        ):
            self.recuperar_comando()
            return False

        return self.consumir(
            self.TERMINAL,
            descricao="o terminal 'Uai' ou 'uai' após 'Fala_tu(...)'"
        ) is not None

    # ---------------------------------------------------------
    # sepa/vorta := KW '(' condicao ')' bloco TERMINAL
    # ---------------------------------------------------------
    def sepa(self):
        self.avancar()
        return self.estrutura_condicional()

    def vorta(self):
        self.avancar()
        return self.estrutura_condicional()

    def estrutura_condicional(self):
        sucesso = True

        if not self.consumir(
            self.CARACTERE, "(", "o caractere '('"
        ):
            sucesso = False

        if not self.condicao():
            self.registrar_erro("esperava uma condição válida")
            sucesso = False

        if not self.consumir(
            self.CARACTERE, ")", "o caractere ')'"
        ):
            sucesso = False

        if not self.bloco():
            sucesso = False

        if not self.consumir(
            self.TERMINAL,
            descricao="o terminal 'Uai' ou 'uai' após o bloco"
        ):
            sucesso = False

        return sucesso

    # ---------------------------------------------------------
    # bloco := '{[' comando* ']}'
    # ---------------------------------------------------------
    def bloco(self):
        if not self.consumir(
            self.ESCOPO, "{[",
            "a abertura de escopo '{['"
        ):
            return False

        sucesso = True

        while (self.token_atual() is not None
               and not self.eh(self.ESCOPO, "]}")):
            if not self.comando():
                token = self.token_atual()
                if token is None:
                    break
                self.registrar_erro(
                    f"esperava um comando válido dentro do bloco, "
                    f"mas encontrou '{token['valor']}'",
                    token
                )
                self.recuperar_comando()
                sucesso = False

        if not self.consumir(
            self.ESCOPO, "]}",
            "o fechamento de escopo ']}'"
        ):
            sucesso = False

        return sucesso

    # ---------------------------------------------------------
    # condicao := expressao relacional expressao
    #            (logico expressao relacional expressao)*
    # ---------------------------------------------------------
    def condicao(self):
        if not self.expressao():
            return False

        if not self.eh_operador_relacional():
            return False

        self.avancar()

        if not self.expressao():
            return False

        while self.eh_operador_logico():
            self.avancar()

            if not self.expressao():
                return False

            if self.eh_operador_relacional():
                self.avancar()
                if not self.expressao():
                    return False

        return True

    # ---------------------------------------------------------
    # expressao := termo (('+' | '-') termo)*
    # termo     := fator (('*' | '/') fator)*
    # fator     := NUMERAL | VAR | '(' expressao ')'
    # ---------------------------------------------------------
    def expressao(self):
        if not self.termo():
            return False

        while self.eh_operador_aritmetico("+", "-"):
            self.avancar()
            if not self.termo():
                return False

        return True

    def termo(self):
        if not self.fator():
            return False

        while self.eh_operador_aritmetico("*", "/"):
            self.avancar()
            if not self.fator():
                return False

        return True

    def fator(self):
        if self.eh_numero() or self.eh_variavel():
            # Operadores lógicos só são válidos dentro de condições.
            if self.eh_operador_logico():
                return False
            self.avancar()
            return True

        if self.eh(self.CARACTERE, "("):
            self.avancar()
            if not self.expressao():
                return False
            return self.consumir(
                self.CARACTERE, ")",
                "o caractere ')'"
            ) is not None

        return False

    # ---------------------------------------------------------
    # Recuperação simples para continuar diagnosticando
    # ---------------------------------------------------------
    def recuperar_comando(self):
        sincronizacao = {
            "Trem", "trem",
            "Fala_tu", "fala_tu",
            "Sepa", "sepa",
            "Vorta", "vorta",
            "Uai", "uai",
            "]}",
        }

        while self.token_atual() is not None:
            valor = self.token_atual()["valor"]
            token = self.token_atual()

            if valor in {"Uai", "uai"}:
                self.avancar()
                return

            if valor == "]}":
                return

            if valor in sincronizacao:
                return

            # Uma variável no começo de uma nova linha pode ser o início
            # de uma nova atribuição. Não consuma esse token durante a
            # recuperação de um erro da linha anterior.
            if (token["tipo"] == self.VARIAVEL and
                    self.posicao_atual > 0 and
                    token["linha"] > self.tokens[self.posicao_atual - 1]["linha"]):
                return

            self.avancar()

# =========================================================
# 3. INICIALIZAÇÃO DO PROGRAMA
# =========================================================
if __name__ == "__main__":
    raiz = tk.Tk()
    app = Interface(raiz)
    raiz.mainloop()