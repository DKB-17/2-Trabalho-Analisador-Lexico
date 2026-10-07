import sys 
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext 
import re

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
            ('TERMINAL', r'(?i)uai'),             
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
        self.janela.geometry("900x500") 
        self.lexer = LexerSertaLanguage() 
        self.caminho_selecionado = ""

        # --- 1. PAINEL SUPERIOR (Botões de Ação) ---
        frame_top = tk.Frame(self.janela)
        frame_top.pack(fill=tk.X, padx=10, pady=10)

        self.botao_selecionar = tk.Button(frame_top, text="📂 1. Escolher Arquivo", command=self.escolher_arquivo)
        self.botao_selecionar.pack(side=tk.LEFT, padx=5)

        self.botao_enviar = tk.Button(frame_top, text="🚀 2. Analisar Código", command=self.enviar_arquivo)
        self.botao_enviar.pack(side=tk.LEFT, padx=5)

        self.label_info = tk.Label(frame_top, text="Nenhum arquivo selecionado.")
        self.label_info.pack(side=tk.LEFT, padx=15)

        # --- 2. PAINEL CENTRAL 
        frame_meio = tk.PanedWindow(self.janela, orient=tk.HORIZONTAL)
        frame_meio.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame_codigo = tk.LabelFrame(frame_meio, text="Código Fonte (.txt)")
        self.area_codigo = scrolledtext.ScrolledText(frame_codigo, width=40, font=("Courier", 10))
        self.area_codigo.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame_meio.add(frame_codigo)

        frame_saida = tk.LabelFrame(frame_meio, text="Console de Compilação")
        self.area_saida = scrolledtext.ScrolledText(frame_saida, width=50, font=("Consolas", 10), bg="#1E1E1E", fg="#00FF00")
        self.area_saida.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame_meio.add(frame_saida)

        class RedirecionadorPrint:
            def __init__(self, widget):
                self.widget = widget

                
                self.widget.tag_config("verde", foreground="#00FF00")     
                self.widget.tag_config("vermelho", foreground="#FF5555")  
                self.widget.tag_config("amarelo", foreground="#FFD700")   


            def write(self, texto):
                if "ERRO" in texto or "Erro" in texto or "[ERRO]" in texto:
                    self.widget.insert(tk.END, texto, "vermelho")
                
                elif "RESULTADO" in texto or "===" in texto or "Resumo" in texto:
                    self.widget.insert(tk.END, texto, "amarelo")
                
                else:
                    self.widget.insert(tk.END, texto, "verde")
                    
                self.widget.see(tk.END) 
            def flush(self): pass

        sys.stdout = RedirecionadorPrint(self.area_saida)

    def escolher_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo SertaLanguage",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.caminho_selecionado = caminho
            nome_arquivo = caminho.split('/')[-1] 
            self.label_info.config(text=f"Arquivo selecionado: {nome_arquivo}")
            
            try:
                with open(caminho, 'r', encoding='utf-8') as arquivo:
                    conteudo = arquivo.read()
                self.area_codigo.delete('1.0', tk.END) 
                self.area_codigo.insert(tk.END, conteudo) 
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler arquivo: {e}")

    def enviar_arquivo(self):
        conteudo_codigo = self.area_codigo.get('1.0', tk.END).strip()

        if conteudo_codigo == "":
            messagebox.showwarning("Aviso", "O código fonte está vazio. Selecione um arquivo ou digite algo.")
            return

        self.area_saida.delete('1.0', tk.END)

        try:
            lista_de_tokens = self.lexer.analisar(conteudo_codigo)
            
            # 2. Sintático (Ativado!)
            #sintatico = AnalisadorSintatico(lista_de_tokens)
            #sintatico.analisar()
            
        except Exception as erro:
            print(f"\nERRO FATAL NA COMPILAÇÃO:\n{erro}")

            
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