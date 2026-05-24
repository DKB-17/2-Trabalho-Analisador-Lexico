# Analisador Léxico com Autômato Finito (DFA) e Visualização de Grafos

## 📋 Visão Geral

O arquivo `analisador_lexico_com_grafo.py` implementa um **analisador léxico completo** baseado em um **autômato finito determinístico (DFA)**, com capacidade de:

1. **Ler arquivos de entrada** fornecidos pelo usuário
2. **Tokenizar código** linha a linha seguindo transições de estados
3. **Gerar relatório detalhado** com Token, Tipo, Valor e Posição (linha, coluna)
4. **Visualizar grafos** do autômato e da leitura em forma de arvore
5. **Salvar grafos como PNG** para análise visual

---

## 🏗️ Estrutura do Código

### 1. **Classe `Token`** (Dataclass)

```python
@dataclass
class Token:
    tipo: str      # Ex: "PALAVRA_RESERVADA", "IDENTIFICADOR", "NUMERO"
    valor: str     # Ex: "receita", "x", "10"
    linha: int     # Linha no arquivo (1-indexed)
    coluna: int    # Coluna no arquivo (1-indexed)
```

Cada token representa uma unidade léxica reconhecida pelo analisador.

### 2. **Classe `AnalisadorLexicoComGrafo`**

#### Atributos de Classe

- **`PALAVRAS_RESERVADAS`**: Conjunto de palavras-chave da linguagem
  - `receita`, `trem`, `entrega`, `sepa`, `vixe`, `hum`, `vorta`
  
- **`OPERADORES_ARITMETICOS`**: `{"+", "-", "*", "/"}`

- **`DELIMITADORES`**: `{"(", ")", "{", "}", ",", ";"}`

#### Atributo de Instância

- **`self.grafo`**: Dicionário representando o **autômato finito**
  - Chave: estado atual (ex: `"START"`, `"ID"`, `"NUM"`)
  - Valor: dicionário mapeando entrada → próximo estado

#### Estrutura do Grafo

```
START
├─ LETRA → ID
├─ DIGITO → NUM
├─ " → STRING_DQ
├─ # → COMMENT
└─ = → ATRIB_OR_EQ

ID (estado para identificadores/palavras-chave)
├─ LETRA → ID        (continua lendo letras)
├─ DIGITO → ID       (também aceita dígitos)
└─ _ → ID            (e underscores)

NUM (estado para números inteiros)
├─ DIGITO → NUM      (continua lendo dígitos)
└─ . → NUM_DOT       (inicia número decimal)

NUM_DOT (ponto de número decimal)
└─ DIGITO → NUM_DEC  (deve ter dígito após ponto)

NUM_DEC (número decimal)
└─ DIGITO → NUM_DEC  (continua com dígitos decimais)

... (outros estados para operadores, strings, comentários)
```

---

## 🔄 Fluxo de Tokenização (Algoritmo DFA)

O método `analisar()` implementa um autômato finito atuando desta maneira:

### Pseudocódigo

```
1. Inicializar: estado = START, lexema = "", posição = 0
2. Para cada caractere do texto:
   a. Se espaço/tabulação → pular (ignorar)
   b. Se quebra de linha → incrementar linha, resetar coluna
   c. Obter classe do caractere (letra, digit, operador, etc.)
   d. Procurar transição: grafo[estado][classe] → próximo_estado
   e. Se transição existe:
      - Mover para próximo_estado
      - Acumular caractere em lexema
   f. Se não existe transição:
      - Emitir token com tipo apropriado
      - Resetar estado para START
      - Voltar ao passo anterior sem consumir caractere
3. Ao fim do arquivo: emitir token final se houver lexema pendente
```

### Exemplo Prático

**Entrada**: `Trem x = 10`

| Estado | Caract | Classe | Próximo | Ação |
|--------|--------|--------|---------|------|
| START | T | LETRA | ID | Acumular 'T' em lexema |
| ID | r | LETRA | ID | Acumular 'r' em lexema |
| ID | e | LETRA | ID | Acumular 'e' em lexema |
| ID | m | LETRA | ID | Acumular 'm' em lexema |
| ID | (espaço) | - | - | Emitir Token("PALAVRA_RESERVADA", "Trem") |
| START | x | LETRA | ID | Acumular 'x' em lexema |
| ID | (espaço) | - | - | Emitir Token("IDENTIFICADOR", "x") |
| START | = | = | ATRIB_OR_EQ | Acumular '=' em lexema |
| ATRIB_OR_EQ | (espaço) | - | - | Emitir Token("OPERADOR_ATRIBUICAO", "=") |
| START | 1 | DIGITO | NUM | Acumular '1' em lexema |
| NUM | 0 | DIGITO | NUM | Acumular '0' em lexema |
| NUM | (fim) | - | - | Emitir Token("NUMERO", "10") |

**Saída**: 5 tokens
- `Token("PALAVRA_RESERVADA", "Trem", L1, C1)`
- `Token("IDENTIFICADOR", "x", L1, C6)`
- `Token("OPERADOR_ATRIBUICAO", "=", L1, C8)`
- `Token("NUMERO", "10", L1, C10)`

---

## 📊 Visualização de Grafos

### 1. **Grafo do Autômato**

Mostra todos os estados e transições do DFA em forma visual:

```
START
 ├─→ ID (entrada: LETRA)
 ├─→ NUM (entrada: DIGITO)
 ├─→ STRING_DQ (entrada: ")
 └─→ OPERADOR_ATRIBUICAO (entrada: =)

ID
 ├─→ ID (entrada: LETRA)
 ├─→ ID (entrada: DIGITO)
 └─→ ID (entrada: _)

... e assim por diante
```

Gerado pelo método: `construir_grafo_automato()`

### 2. **Árvore da Leitura**

Hierarquia da análise do arquivo:

```
ARQUIVO
 ├─ LINHA_1
 │  ├─ T1:PALAVRA_RESERVADA:Trem
 │  ├─ T2:IDENTIFICADOR:x
 │  ├─ T3:OPERADOR_ATRIBUICAO:=
 │  └─ T4:NUMERO:10
 ├─ LINHA_2
 │  ├─ T5:PALAVRA_RESERVADA:Trem
 │  ├─ T6:IDENTIFICADOR:y
 │  ├─ T7:OPERADOR_ATRIBUICAO:=
 │  └─ T8:NUMERO:5
 └─ LINHA_3
    ├─ T9:IDENTIFICADOR:z
    ├─ T10:OPERADOR_ATRIBUICAO:=
    ├─ T11:IDENTIFICADOR:x
    ├─ T12:OPERADOR_ARITMETICO:+
    └─ T13:IDENTIFICADOR:y
```

Gerado pelo método: `construir_arvore_tokens()`

---

## 🚀 Como Usar

### Pré-requisitos

```bash
pip install networkx matplotlib
```

### Execução

1. Abra um terminal na pasta do projeto
2. Execute o script:

```bash
.\venv\Scripts\python.exe analisador_lexico_com_grafo.py
```

3. O programa solicitará:

```
Informe o caminho do arquivo de entrada (.txt): 
```

4. Forneça o caminho (ex: `exemplo_teste.txt`)

5. O programa mostrará:
   - **Grafo de transições do autômato** (em texto)
   - **Relatório de tokens** com formato: TOKEN | TIPO | VALOR | POSIÇÃO

6. Perguntará se deseja visualizar grafos:
```
Deseja visualizar os grafos? (s/n): 
```

7. Se sim, escolha:
```
Salvar grafos como PNG em vez de exibir na tela? (s/n):
```

8. Forneça um prefixo para os nomes dos arquivos PNG:
```
Prefixo para nomes dos grafos (deixe vazio para usar nome do arquivo):
```

### Exemplo Completo

```bash
Informe o caminho do arquivo de entrada (.txt): exemplo_teste.txt
Deseja visualizar os grafos? (s/n): s
Salvar grafos como PNG em vez de exibir na tela? (s/n): s
Prefixo para nomes dos grafos (deixe vazio para usar nome do arquivo): meu_analise

# Resultado:
Grafo salvo em: meu_analise_automato.png
Grafo salvo em: meu_analise_arvore.png
```

---

## 📝 Relatório de Saída

### Formato

```
TOKEN           TIPO                    VALOR           POSIÇÃO
Trem            PALAVRA_RESERVADA       Trem            L1,C1
cheio           IDENTIFICADOR           cheio           L1,C6
x               IDENTIFICADOR           x               L1,C12
=               OPERADOR_ATRIBUICAO     =               L1,C14
10              NUMERO                  10              L1,C16
```

### Interpretação

- **TOKEN**: O valor textual do token
- **TIPO**: Classificação (PALAVRA_RESERVADA, IDENTIFICADOR, NUMERO, etc.)
- **VALOR**: Valor do token (redundante com TOKEN por agora)
- **POSIÇÃO**: Localização no arquivo (linha, coluna) - 1-indexed

---

## 🔧 Métodos Principais

### `analisar(texto: str) -> List[Token]`
Tokeniza um texto em memória usando o DFA.

### `analisar_arquivo(caminho_arquivo: str) -> List[Token]`
Lê arquivo e tokeniza seu conteúdo.

### `exibir_grafo()`
Imprime no console o grafo do autômato em formato texto.

### `construir_grafo_automato() -> nx.DiGraph`
Retorna o grafo do autômato em formato NetworkX.

### `construir_arvore_tokens(tokens: List[Token]) -> nx.DiGraph`
Constrói árvore hierárquica dos tokens por linha.

### `desenhar_grafo(grafo, titulo, salvar_como=None)`
Desenha grafo usando Matplotlib e NetworkX.
- Se `salvar_como` for None: tenta exibir janela interativa (ou salva em `grafo_temp.png` se falhar)
- Se `salvar_como` for caminho: salva como PNG nesse caminho

---

## 📊 Tipos de Tokens Reconhecidos

| Tipo | Exemplos |
|------|----------|
| PALAVRA_RESERVADA | receita, trem, entrega, sepa, vixe, hum, vorta |
| IDENTIFICADOR | x, y, nome, contador, _variavel |
| NUMERO | 10, 3.14, 100, 0.5 |
| OPERADOR_ARITMETICO | +, -, *, / |
| OPERADOR_ATRIBUICAO | = |
| OPERADOR_RELACIONAL | <, >, <=, >=, ==, != |
| STRING | "texto", 'texto' |
| DELIMITADOR | (, ), {, }, ,, ; |
| COMENTARIO | # comentário (ignorado) |
| ERRO | caractere inválido |

---

## 🎯 Casos de Uso

1. **Validação de sintaxe**: Verificar se arquivo segue estrutura esperada
2. **IDE/Editor**: Fornecer tokens para syntax highlighting
3. **Parser**: Base para análise sintática posterior
4. **Documentação**: Visualizar fluxo de processamento
5. **Debugging**: Entender como código é tokenizado

---

## 📚 Comparação: Biblioteca SLY vs Autômato Manual

| Aspecto | SLY | Autômato Manual |
|---------|-----|-----------------|
| **Facilidade** | Muito fácil (declarativo) | Médio (imperativo) |
| **Flexibilidade** | Média | Alta |
| **Controle** | Limitado | Total |
| **Visualização** | Nenhuma nativa | Podemos adicionar grafos |
| **Performance** | Muito rápida (otimizada) | Boa (nossa implementação) |
| **Aprendizado** | Conceitos ocultos | Entende-se o algoritmo |

---

## 🔗 Referências

- **DFA (Deterministic Finite Automaton)**: Máquina de estados finita determinística
- **Lexer/Scanner**: Analisador léxico (primeira fase de compilação)
- **NetworkX**: Biblioteca Python para grafos dirigidos
- **Matplotlib**: Visualização em Python

---

## 💡 Possíveis Melhorias

1. Adicionar suporte a tokens da SertaLanguage ({[, ]}, Uai, pau_a_pau, miúdo, etc.)
2. Integração com parser sintático
3. Geração de AST (Abstract Syntax Tree)
4. Relatório de erros léxicos mais detalhado
5. Interface gráfica (Tkinter) integrada
6. Exportação de relatórios em JSON/CSV

---

## 📞 Contato

Para dúvidas sobre o funcionamento do analisador, consulte os comentários no código ou execute:

```bash
.\venv\Scripts\python.exe analisador_lexico_com_grafo.py
```

E escolha visualizar os grafos para entender melhor as transições!
