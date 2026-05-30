from dataclasses import dataclass
import csv
from pathlib import Path
from typing import Dict, List, Set

try:
    import matplotlib.pyplot as plt
    import networkx as nx
except ImportError:  # Dependencias opcionais para exibicao visual do grafo
    plt = None
    nx = None


@dataclass
class Token:
    tipo: str
    valor: str
    linha: int
    coluna: int


class AnalisadorLexicoComGrafo:
    """Lexer simples implementado como automato finito deterministico (DFA)."""

    PALAVRAS_RESERVADAS: Set[str] = {
        "receita",
        "trem",
        "bisbilhota",
        "fala_tu",
        "entrega",
        "meteope",
        "sepa",
        "vixe",
        "hum",
        "vorta",
    }

    OPERADORES_LOGICOS: Set[str] = {
        "nem_a_pau",
        "tambem",
        "também",
        "ou",
    }

    TIPOS_DADOS: Set[str] = {
        "cheio",
        "quebrado",
        "prosa",
        "confuso",
        "domino",
        "oco",
        "bagulho",
    }

    CARACTERES_ESPECIAIS_PALAVRA: Set[str] = {
        "uai",
    }

    OPERADORES_ATRIBUICAO: Set[str] = {"="}
    OPERADORES_ARITMETICOS: Set[str] = {"+", "-", "*", "/"}
    OPERADORES_RELACIONAIS: Set[str] = {"<", ">"}
    OPERADORES: Set[str] = OPERADORES_ATRIBUICAO | OPERADORES_ARITMETICOS | OPERADORES_RELACIONAIS
    DELIMITADORES: Set[str] = {"(", ")", "{", "}", ",", ";"}

    def __init__(self) -> None:
        # Grafo do automato: estado -> classe_de_entrada -> proximo_estado
        self.grafo: Dict[str, Dict[str, str]] = {
            "START": {
                "LETRA": "ID",
                "_": "ID",
                "DIGITO": "NUM",
                "\"": "STRING_DQ",
                "'": "STRING_SQ",
                "#": "COMMENT",
            },
            "ID": {
                "LETRA": "ID",
                "DIGITO": "ID",
                "_": "ID",
            },
            "NUM": {
                "DIGITO": "NUM",
                ".": "NUM_DOT",
            },
            "NUM_DOT": {
                "DIGITO": "NUM_DEC",
            },
            "NUM_DEC": {
                "DIGITO": "NUM_DEC",
            },
            "STRING_DQ": {
                "\"": "START",
            },
            "STRING_SQ": {
                "'": "START",
            },
            "COMMENT": {
                "\\n": "START",
            },
        }

    def analisar(self, texto: str, incluir_tokens_ocultos: bool = False) -> List[Token]:
        tokens: List[Token] = []

        i = 0
        linha = 1
        coluna = 1
        estado = "START"
        lexema = ""
        inicio_linha = 1
        inicio_coluna = 1

        while i < len(texto):
            c = texto[i]

            if estado == "START":
                if c in " \t\r":
                    if incluir_tokens_ocultos:
                        inicio_linha = linha
                        inicio_coluna = coluna
                        inicio = i
                        while i < len(texto) and texto[i] in " \t\r":
                            i += 1
                            coluna += 1
                        tokens.append(Token("ESPACO_EM_BRANCO", texto[inicio:i], inicio_linha, inicio_coluna))
                        continue
                    i += 1
                    coluna += 1
                    continue

                if c == "\n":
                    i += 1
                    linha += 1
                    coluna = 1
                    continue

                if c == "#":
                    inicio_linha = linha
                    inicio_coluna = coluna
                    inicio = i
                    while i < len(texto) and texto[i] != "\n":
                        i += 1
                        coluna += 1
                    if incluir_tokens_ocultos:
                        tokens.append(Token("COMENTARIO", texto[inicio:i], inicio_linha, inicio_coluna))
                    continue

                inicio_linha = linha
                inicio_coluna = coluna

                if texto.startswith("{[", i):
                    tokens.append(Token("CARACTERE_ESPECIAL", "{[", inicio_linha, inicio_coluna))
                    i += 2
                    coluna += 2
                    continue

                if texto.startswith("]}", i):
                    tokens.append(Token("CARACTERE_ESPECIAL", "]}", inicio_linha, inicio_coluna))
                    i += 2
                    coluna += 2
                    continue

                classe = self._classe_char(c)
                proximo = self.grafo["START"].get(classe)

                if proximo == "ID":
                    estado = "ID"
                    lexema = c
                    i += 1
                    coluna += 1
                    continue

                if proximo == "NUM":
                    estado = "NUM"
                    lexema = c
                    i += 1
                    coluna += 1
                    continue

                if proximo in {"STRING_DQ", "STRING_SQ"}:
                    estado = proximo
                    lexema = c
                    i += 1
                    coluna += 1
                    continue

                if proximo == "COMMENT":
                    estado = "COMMENT"
                    i += 1
                    coluna += 1
                    continue

                if c in self.OPERADORES_ATRIBUICAO:
                    tokens.append(Token("OPERADOR_ATRIBUICAO", c, inicio_linha, inicio_coluna))
                    i += 1
                    coluna += 1
                    continue

                if c in self.OPERADORES_ARITMETICOS:
                    tokens.append(Token("OPERADOR_ARITMETICO", c, inicio_linha, inicio_coluna))
                    i += 1
                    coluna += 1
                    continue

                if c in self.OPERADORES_RELACIONAIS:
                    tokens.append(Token("OPERADOR_RELACIONAL", c, inicio_linha, inicio_coluna))
                    i += 1
                    coluna += 1
                    continue

                if c in self.DELIMITADORES:
                    tokens.append(Token("CARACTERE_ESPECIAL", c, inicio_linha, inicio_coluna))
                    i += 1
                    coluna += 1
                    continue

                tokens.append(Token("ERRO", f"Caractere invalido: {c}", inicio_linha, inicio_coluna))
                i += 1
                coluna += 1
                continue

            if estado == "ID":
                classe = self._classe_char(c)
                if self.grafo["ID"].get(classe) == "ID":
                    lexema += c
                    i += 1
                    coluna += 1
                    continue

                tipo = self._classificar_identificador(lexema)
                tokens.append(Token(tipo, lexema, inicio_linha, inicio_coluna))
                estado = "START"
                lexema = ""
                continue

            if estado == "NUM":
                classe = self._classe_char(c)
                proximo = self.grafo["NUM"].get(classe)
                if proximo == "NUM":
                    lexema += c
                    i += 1
                    coluna += 1
                    continue
                if proximo == "NUM_DOT":
                    lexema += c
                    estado = "NUM_DOT"
                    i += 1
                    coluna += 1
                    continue

                tokens.append(Token("NUMERAL", lexema, inicio_linha, inicio_coluna))
                estado = "START"
                lexema = ""
                continue

            if estado == "NUM_DOT":
                classe = self._classe_char(c)
                if self.grafo["NUM_DOT"].get(classe) == "NUM_DEC":
                    lexema += c
                    estado = "NUM_DEC"
                    i += 1
                    coluna += 1
                    continue

                tokens.append(Token("ERRO", f"Numero decimal invalido: {lexema}", inicio_linha, inicio_coluna))
                estado = "START"
                lexema = ""
                continue

            if estado == "NUM_DEC":
                classe = self._classe_char(c)
                if self.grafo["NUM_DEC"].get(classe) == "NUM_DEC":
                    lexema += c
                    i += 1
                    coluna += 1
                    continue

                tokens.append(Token("NUMERAL", lexema, inicio_linha, inicio_coluna))
                estado = "START"
                lexema = ""
                continue

            if estado == "STRING_DQ":
                lexema += c
                i += 1
                if c == "\n":
                    linha += 1
                    coluna = 1
                else:
                    coluna += 1

                if c == "\"":
                    tokens.append(Token("STRING", lexema, inicio_linha, inicio_coluna))
                    estado = "START"
                    lexema = ""
                continue

            if estado == "STRING_SQ":
                lexema += c
                i += 1
                if c == "\n":
                    linha += 1
                    coluna = 1
                else:
                    coluna += 1

                if c == "'":
                    tokens.append(Token("STRING", lexema, inicio_linha, inicio_coluna))
                    estado = "START"
                    lexema = ""
                continue

            if estado == "COMMENT":
                if c == "\n":
                    estado = "START"
                    linha += 1
                    coluna = 1
                    i += 1
                    continue

                i += 1
                coluna += 1
                continue

        # Finalizacao em fim de arquivo
        if estado == "ID":
            tipo = self._classificar_identificador(lexema)
            tokens.append(Token(tipo, lexema, inicio_linha, inicio_coluna))
        elif estado in {"NUM", "NUM_DEC"}:
            tokens.append(Token("NUMERAL", lexema, inicio_linha, inicio_coluna))
        elif estado == "NUM_DOT":
            tokens.append(Token("ERRO", f"Numero decimal invalido: {lexema}", inicio_linha, inicio_coluna))
        elif estado in {"STRING_DQ", "STRING_SQ"}:
            tokens.append(Token("ERRO", "String nao finalizada", inicio_linha, inicio_coluna))

        return tokens

    def analisar_arquivo(self, caminho_arquivo: str, incluir_tokens_ocultos: bool = False) -> List[Token]:
        conteudo = Path(caminho_arquivo).read_text(encoding="utf-8")
        return self.analisar(conteudo, incluir_tokens_ocultos=incluir_tokens_ocultos)

    @staticmethod
    def _classe_char(c: str) -> str:
        if c.isalpha():
            return "LETRA"
        if c.isdigit():
            return "DIGITO"
        return c

    def _classificar_identificador(self, lexema: str) -> str:
        valor = lexema.lower()
        if valor in self.PALAVRAS_RESERVADAS:
            return "PALAVRA_RESERVADA"
        if valor in self.OPERADORES_LOGICOS:
            return "OPERADOR_LOGICO"
        if valor in self.TIPOS_DADOS:
            return "TIPO_DADOS"
        if valor in self.CARACTERES_ESPECIAIS_PALAVRA:
            return "CARACTERE_ESPECIAL"
        return "VARIAVEIS"

    def exibir_grafo(self) -> None:
        print("Grafo de transicoes (estado --entrada--> proximo_estado):")
        for estado, transicoes in self.grafo.items():
            for entrada, destino in transicoes.items():
                print(f"  {estado} --{entrada}--> {destino}")

    def construir_grafo_automato(self):
        if nx is None:
            return None

        grafo = nx.DiGraph()
        for estado, transicoes in self.grafo.items():
            grafo.add_node(estado)
            for entrada, destino in transicoes.items():
                grafo.add_edge(estado, destino, label=entrada)
        return grafo

    def construir_arvore_tokens(self, tokens: List[Token]):
        if nx is None:
            return None

        arvore = nx.DiGraph()
        raiz = "ARQUIVO"
        arvore.add_node(raiz)

        linhas = sorted({t.linha for t in tokens})
        for linha in linhas:
            no_linha = f"LINHA_{linha}"
            arvore.add_node(no_linha)
            arvore.add_edge(raiz, no_linha)

        for idx, token in enumerate(tokens, start=1):
            no_token = f"T{idx}:{token.tipo}:{token.valor}"
            no_linha = f"LINHA_{token.linha}"
            arvore.add_node(no_token)
            arvore.add_edge(no_linha, no_token)

        return arvore

    @staticmethod
    def validar_delimitadores_com_pilha(tokens: List[Token]):
        pares = {
            "(": ")",
            "{": "}",
            "[": "]",
            "{[": "]}",
        }
        fechamentos = {v: k for k, v in pares.items()}

        pilha = []
        erros = []

        for token in tokens:
            if token.tipo != "CARACTERE_ESPECIAL":
                continue

            valor = token.valor
            if valor in pares:
                pilha.append(token)
                continue

            if valor in fechamentos:
                if not pilha:
                    erros.append(f"Fechamento inesperado '{valor}' em L{token.linha},C{token.coluna}")
                    continue

                topo = pilha.pop()
                esperado = pares[topo.valor]
                if valor != esperado:
                    erros.append(
                        f"Delimitador invalido em L{token.linha},C{token.coluna}: esperado '{esperado}' para '{topo.valor}' aberto em L{topo.linha},C{topo.coluna}"
                    )

        while pilha:
            topo = pilha.pop()
            esperado = pares[topo.valor]
            erros.append(
                f"Delimitador nao fechado '{topo.valor}' em L{topo.linha},C{topo.coluna}. Esperado '{esperado}'"
            )

        return len(erros) == 0, erros

    @staticmethod
    def desenhar_grafo(grafo, titulo: str, salvar_como: str = None) -> None:
        if nx is None or plt is None:
            print("Visualizacao indisponivel. Instale: pip install networkx matplotlib")
            return

        if grafo is None or grafo.number_of_nodes() == 0:
            print("Grafo vazio, nada para desenhar.")
            return

        plt.figure(figsize=(14, 8))

        try:
            # Melhor layout para estruturas em arvore quando Graphviz/pydot estiver disponivel
            from networkx.drawing.nx_pydot import graphviz_layout

            pos = graphviz_layout(grafo, prog="dot")
        except Exception:
            pos = nx.spring_layout(grafo, seed=7)

        nx.draw_networkx_nodes(grafo, pos, node_size=1800, node_color="#B7E4C7")
        nx.draw_networkx_edges(grafo, pos, arrows=True, arrowsize=18, edge_color="#2D6A4F")
        nx.draw_networkx_labels(grafo, pos, font_size=8)

        labels_arestas = nx.get_edge_attributes(grafo, "label")
        if labels_arestas:
            nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels_arestas, font_size=7)

        plt.title(titulo)
        plt.axis("off")
        plt.tight_layout()

        if salvar_como:
            plt.savefig(salvar_como, dpi=150, bbox_inches="tight")
            print(f"Grafo salvo em: {salvar_como}")
        else:
            try:
                plt.show()
            except Exception as e:
                print(f"Nao foi possivel exibir grafo na tela: {e}")
                print("Salvando como 'grafo_temp.png' em vez disso...")
                plt.savefig("grafo_temp.png", dpi=150, bbox_inches="tight")
                print("Grafo salvo em: grafo_temp.png")

        plt.close()


def imprimir_relatorio_tokens(tokens: List[Token]) -> None:
    print("\nRelatorio de saida (Token, Tipo, Valor):")
    print("TOKEN\t\tTIPO\t\t\tVALOR\t\tPOSICAO")
    for token in tokens:
        print(f"{token.valor}\t\t{token.tipo}\t\t{token.valor}\t\tL{token.linha},C{token.coluna}")


def exportar_relatorio_tokens(tokens: List[Token], prefixo: str, delimitadores_ok: bool, erros_delimitadores: List[str]) -> None:
    caminho_txt = f"{prefixo}_relatorio_lexico.txt"
    caminho_csv = f"{prefixo}_relatorio_lexico.csv"

    with open(caminho_txt, "w", encoding="utf-8") as arquivo_txt:
        arquivo_txt.write("Relatorio de saida (Token, Tipo, Valor)\n")
        arquivo_txt.write("TOKEN\tTIPO\tVALOR\tPOSICAO\n")
        for token in tokens:
            arquivo_txt.write(f"{token.valor}\t{token.tipo}\t{token.valor}\tL{token.linha},C{token.coluna}\n")

        arquivo_txt.write("\nValidacao de delimitadores por pilha:\n")
        arquivo_txt.write(f"STATUS: {'OK' if delimitadores_ok else 'FALHA'}\n")
        if erros_delimitadores:
            arquivo_txt.write("Erros:\n")
            for erro in erros_delimitadores:
                arquivo_txt.write(f"- {erro}\n")

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["TOKEN", "TIPO", "VALOR", "LINHA", "COLUNA"])
        for token in tokens:
            writer.writerow([token.valor, token.tipo, token.valor, token.linha, token.coluna])

    print(f"Relatorios exportados: {caminho_txt} e {caminho_csv}")


def obter_caminho_input() -> str:
    caminho = input("Informe o caminho do arquivo de entrada (.txt): ").strip().strip('"')
    if not caminho:
        raise ValueError("Nenhum caminho informado.")
    if not Path(caminho).exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")
    return caminho


if __name__ == "__main__":
    analisador = AnalisadorLexicoComGrafo()

    try:
        caminho_arquivo = obter_caminho_input()
        tokens = analisador.analisar_arquivo(caminho_arquivo)
    except Exception as erro:
        print(f"Erro ao ler/analisar arquivo: {erro}")
        raise SystemExit(1)

    analisador.exibir_grafo()
    imprimir_relatorio_tokens(tokens)

    delimitadores_ok, erros_delimitadores = analisador.validar_delimitadores_com_pilha(tokens)
    print("\nValidacao de delimitadores por pilha:")
    print(f"STATUS: {'OK' if delimitadores_ok else 'FALHA'}")
    if erros_delimitadores:
        for erro in erros_delimitadores:
            print(f"  - {erro}")

    prefixo_relatorio = Path(caminho_arquivo).stem
    exportar_relatorio_tokens(tokens, prefixo_relatorio, delimitadores_ok, erros_delimitadores)

    # Pergunta se usuario quer visualizar grafos
    resposta = input("\nDeseja visualizar os grafos? (s/n): ").strip().lower()
    if resposta in {"s", "sim", "y", "yes"}:
        salvar = input("Salvar grafos como PNG em vez de exibir na tela? (s/n): ").strip().lower()
        prefixo_arquivo = input("Prefixo para nomes dos grafos (deixe vazio para usar nome do arquivo): ").strip()

        if not prefixo_arquivo:
            prefixo_arquivo = Path(caminho_arquivo).stem

        if salvar in {"s", "sim", "y", "yes"}:
            grafo_automato = analisador.construir_grafo_automato()
            arvore_tokens = analisador.construir_arvore_tokens(tokens)

            analisador.desenhar_grafo(grafo_automato, "Grafo do Automato Lexico", f"{prefixo_arquivo}_automato.png")
            analisador.desenhar_grafo(arvore_tokens, "Arvore da Leitura do Arquivo (Linhas e Tokens)", f"{prefixo_arquivo}_arvore.png")
        else:
            grafo_automato = analisador.construir_grafo_automato()
            arvore_tokens = analisador.construir_arvore_tokens(tokens)

            analisador.desenhar_grafo(grafo_automato, "Grafo do Automato Lexico")
            analisador.desenhar_grafo(arvore_tokens, "Arvore da Leitura do Arquivo (Linhas e Tokens)")
    else:
        print("Grafo nao sera exibido.")
