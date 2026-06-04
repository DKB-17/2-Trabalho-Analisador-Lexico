import tkinter as tk
from tkinter import filedialog, messagebox
import re

# =========================================================
# 1. CLASSE DO ANALISADOR LÉXICO (O Motor)
# =========================================================
class LexerSertaLanguage:
    def __init__(self):
        # Palavras Reservadas da linguagem
        self.palavras_reservadas = {
            'Receita', 'Trem', 'Bisbilhota', 'fala_tu', 'Fala_tu', 
            'entrega', 'meteope', 'Sepa', 'hum', 'Hum', 'vixe', 'Vixe', 'Vorta',
            'Dá o grito' # Adicionado conforme seu PDF de exemplo
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
            ('TERMINADOR', r'(?i)uai'),             
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
        print("III) RESULTADO GERADO PELO ANALISADOR LEXICO")
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
                    # Verifica se é uma palavra composta que está nas regras (como "Dá o grito")
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
                elif tipo_regex in ['ESCOPO', 'TERMINADOR', 'CARACTERE_ESP']:
                    tipo_final = "Caractere Especial"
                elif tipo_regex == 'DESCONHECIDO':
                    tipo_final = "ERRO LÉXICO"
                    erros += 1

                resultado_linha += f"Token: {valor} -> {tipo_final}."

                print(f"Linha {numero_linha} | Token: {valor} -> {tipo_final}")
                
                # ---> MUDANÇA AQUI: Guardamos o token no formato de dicionário <---
                lista_tokens.append({
                    'valor': valor,
                    'tipo': tipo_final,
                    'linha': numero_linha
                })
    
        print(f"\nAnálise Léxica Concluída! Total de Linhas: {total_linhas}, Erros Léxicos: {erros}.")
        return lista_tokens     
       


# =========================================================
# 2. CLASSE DA INTERFACE (O Visual)
# =========================================================
class Interface:
    def __init__(self, janela_principal):
        self.janela = janela_principal
        self.janela.title("Analisador Léxico - SertaLanguage")
        self.janela.geometry("400x200")

        # ---> AQUI É O PONTO DE CONEXÃO 1 <---
        # Instanciamos o nosso Lexer real em vez do falso
        self.lexer = LexerSertaLanguage() 
        self.caminho_selecionado = ""

        # Desenho da tela
        self.label_info = tk.Label(self.janela, text="Nenhum arquivo selecionado.")
        self.label_info.pack(pady=20)

        self.botao_selecionar = tk.Button(self.janela, text="1. Escolher Arquivo", command=self.escolher_arquivo)
        self.botao_selecionar.pack(pady=5)

        self.botao_enviar = tk.Button(self.janela, text="2. Analisar Código", command=self.enviar_arquivo)
        self.botao_enviar.pack(pady=5)

    def escolher_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo SertaLanguage",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.caminho_selecionado = caminho
            nome_arquivo = caminho.split('/')[-1] 
            self.label_info.config(text=f"Arquivo pronto: {nome_arquivo}")

    def enviar_arquivo(self):
        if self.caminho_selecionado == "":
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo primeiro!")
            return

        # ---> AQUI É O PONTO DE CONEXÃO 2 <---
        # Lemos o arquivo e passamos o conteúdo direto para o Lexer
        try:
            with open(self.caminho_selecionado, 'r', encoding='utf-8') as arquivo:
                conteudo_codigo = arquivo.read()

            lista_de_tokens = self.lexer.analisar(conteudo_codigo)  # Recebe a lista de tokens do Lexer

            #sintatico = AnalisadorSintatico(lista_de_tokens)

            #sintatico.analisar()
            
            messagebox.showinfo("Sucesso", "Análise concluída!\nVerifique o terminal/console para ver os resultados detalhados.")
            
        except Exception as erro:
            messagebox.showerror("Erro", f"Falha ao tentar ler o arquivo.\nErro: {erro}")

# =========================================================
# 2. CLASSE DO ANALISADOR SINTÁTICO
# =========================================================
class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao_atual = 0
        self.erros = []

    def token_atual(self):
        if self.posicao_atual < len(self.tokens):
            return self.tokens[self.posicao_atual]
        return None

    def consumir(self, tipo_esperado, valor_esperado=None):
        token = self.token_atual()
        
        if token is None:
            self.erros.append(f"Erro: Codigo terminou inesperadamente. Esperava '{tipo_esperado}'.")
            return False

        tipo_bate = token['tipo'] == tipo_esperado
        valor_bate = (valor_esperado is None) or (token['valor'] == valor_esperado)

        if tipo_bate and valor_bate:
            self.posicao_atual += 1
            return True
        else:
            esperado = valor_esperado if valor_esperado else tipo_esperado
            self.erros.append(f"Erro Sintatico na linha {token['linha']}: Encontrou '{token['valor']}', mas esperava '{esperado}'.")
            return False

    def analisar(self):
        print("\n" + "="*50)
        print("IV) RESULTADO DA ANALISE SINTATICA")
        print("="*50)
        
        sucesso = True
        
        # Verifica a assinatura inicial: Receita principal() {[
        if not self.consumir('Palavra Reservada', 'Receita'): sucesso = False
        if not self.consumir('Variável'): sucesso = False
        if not self.consumir('Caractere Especial', '('): sucesso = False
        if not self.consumir('Caractere Especial', ')'): sucesso = False
        if not self.consumir('Caractere Especial', '{['): sucesso = False
        
        if sucesso:
            print("[OK] Estrutura inicial (Receita principal) esta correta!")
        
        # Pula para o final para verificar o fechamento ]} Uai
        if len(self.tokens) >= 2:
            self.posicao_atual = len(self.tokens) - 2 
            
            if not self.consumir('Caractere Especial', ']}'): sucesso = False
            if not self.consumir('Caractere Especial'): sucesso = False # Termina em uai/Uai
            
            if sucesso:
                print("[OK] Estrutura de fechamento (]} Uai) esta correta!")

        if len(self.erros) == 0 and sucesso:
            print("\n[SUCESSO] NENHUM ERRO SINTATICO ENCONTRADO!")
        else:
            print("\n[ERRO] ERROS SINTATICOS ENCONTRADOS:")
            for erro in self.erros:
                print(erro)

# =========================================================
# 3. INICIALIZAÇÃO DO PROGRAMA
# =========================================================
if __name__ == "__main__":
    raiz = tk.Tk()
    app = Interface(raiz)
    raiz.mainloop()