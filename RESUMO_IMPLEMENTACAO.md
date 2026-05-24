## 📚 RESUMO DA IMPLEMENTAÇÃO: ANALISADOR LÉXICO COM AUTÔMATO FINITO E VISUALIZAÇÃO DE GRAFOS

---

### ✅ O QUE FOI IMPLEMENTADO

#### **Arquivo: `analisador_lexico_com_grafo.py`**

1. **Classe `Token` (Dataclass)**
   - Estrutura que encapsula: tipo, valor, linha, coluna
   - Permite identificar exatamente onde cada token aparece no arquivo

2. **Classe `AnalisadorLexicoComGrafo`**
   - Implementa um **Autômato Finito Determinístico (DFA)** completo
   - Lê caractere por caractere e muda de estado conforme regras do grafo
   - Reconhece 9 tipos de tokens:
     - PALAVRA_RESERVADA
     - IDENTIFICADOR
     - NUMERO
     - OPERADOR_ARITMETICO
     - OPERADOR_ATRIBUICAO
     - OPERADOR_RELACIONAL
     - STRING
     - DELIMITADOR
     - COMENTARIO

3. **Métodos de Análise**
   - `analisar(texto)`: Tokeniza texto em memória
   - `analisar_arquivo(caminho)`: Lê arquivo e tokeniza
   - Suporta números inteiros e decimais
   - Suporta strings com aspas simples/duplas
   - Suporta comentários iniciados com #

4. **Métodos de Visualização**
   - `construir_grafo_automato()`: Cria grafo NetworkX do DFA
   - `construir_arvore_tokens()`: Cria hierarquia Arquivo → Linhas → Tokens
   - `desenhar_grafo()`: Renderiza grafos com Matplotlib
     - Salva como PNG se necessário
     - Mostra na tela ou fallback para PNG se sem display

5. **Funções Auxiliares**
   - `imprimir_relatorio_tokens()`: Tabela formatada de tokens
   - `obter_caminho_input()`: Validação de entrada do usuário

---

### 🔄 EVOLUÇÃO DO CÓDIGO

#### **Estágio 1: Implementação Básica do DFA**
- Estrutura de estados e transições
- Loop principal de tokenização
- Reconhecimento de identificadores, números e operadores simples
- ❌ Sem visualização
- ❌ Sem input de arquivo

#### **Estágio 2: Adição de Leitura de Arquivo e Entrada do Usuário**
- Método `analisar_arquivo()` adicionado
- Função `obter_caminho_input()` com validação
- ✅ Usuario pode agora fornecer arquivo como entrada
- ❌ Grafos ainda não implementados

#### **Estágio 3: Construção de Grafos com NetworkX**
- Método `construir_grafo_automato()`: Cria grafo visual do DFA
- Método `construir_arvore_tokens()`: Cria hierarquia da leitura
- Inicialização de Matplotlib/NetworkX com try/except (dependências opcionais)
- ❌ Sem opções de visualização interativa

#### **Estágio 4: Visualização com Matplotlib**
- Método `desenhar_grafo()` completo
- Suporte a salvamento em PNG
- Fallback automático se sem display
- Melhor layout com spring_layout (ou graphviz se disponível)
- ✅ Grafos gerados com sucesso

#### **Estágio 5: Interface Interativa do Usuário**
- Menu de opções para visualizar grafos
- Escolha entre exibir na tela ou salvar como PNG
- Prefixo customizável para nomes de arquivo
- ✅ Fluxo completo implementado

---

### 🎯 FLUXO DE EXECUÇÃO COMPLETO

```
┌─────────────────────────────────────────────────────────────────┐
│                    USUÁRIO EXECUTA PROGRAMA                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │ Solicita caminho do arquivo   │
         │ input(): "arquivo.txt"        │
         └────────────┬──────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ Lê arquivo com Path.read() │
         │ Valida existência          │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────────┐
         │ Chama analisar_arquivo()       │
         │ (que chama analisar())         │
         └────────────┬───────────────────┘
                      │
            ┌─────────┴─────────┐
            │ ALGORITMO DFA     │
            │                   │
    ┌───────▼──────────┐       │
    │ Estado = START   │       │
    └───────┬──────────┘       │
            │                   │
      ┌─────▼──────────────┐   │
      │ Para cada char:    │   │
      │ 1. Classificar     │   │
      │ 2. Procurar        │   │
      │    transição       │   │
      │ 3. Se encontrou:   │   │
      │    Mover estado    │   │
      │ 4. Senão:          │   │
      │    Emitir token    │   │
      │    Reset estado    │   │
      └─────┬──────────────┘   │
            │                   │
            └───────┬───────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │ Retorna List[Token]    │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ Imprime relatório no       │
         │ console (tabela formatada) │
         └────────────┬───────────────┘
                      │
         ┌────────────▼────────────┐
         │ Pergunta: Visualizar    │
         │ grafos? (s/n)           │
         └────┬───────────────┬────┘
              │               │
          "não"              "sim"
              │               │
              ▼               ▼
         ┌─────────────┐  ┌──────────────┐
         │ FIM         │  │ Perguntar:   │
         └─────────────┘  │ Salvar PNG?  │
                         └──┬────────┬───┘
                            │        │
                         "sim"    "não"
                            │        │
                    ┌───────▼┐    ┌──▼──────┐
                    │        │    │         │
                ┌───▼──┐ ┌──▼──┐ │ Exibir  │
                │Salvar│ │Pedir│ │ plt.    │
                │PNG   │ │prefixo  │show()  │
                └─┬────┘ └──┬──┘ │         │
                  │         │    └──┬──────┘
         ┌─────────▼─────────▼──┐   │
         │ construir_grafo_     │   │
         │ automato()           │   │
         │                      │   │
         │ construir_arvore_    │   │
         │ tokens()             │   │
         └─────────┬──────┬─────┘   │
                   │      │         │
         ┌─────────▼──────▼─────┐   │
         │ desenhar_grafo()     │───┘
         │ (com savefig)        │
         └─────────┬────────────┘
                   │
                   ▼
         ┌────────────────────────┐
         │ Salva _automato.png    │
         │ Salva _arvore.png      │
         │                        │
         │ FIM COM SUCESSO        │
         └────────────────────────┘
```

---

### 📊 EXEMPLO REAL DE EXECUÇÃO

**Entrada do Arquivo: `exemplo_teste.txt`**
```
Trem cheio x = 10
Trem quebrado y = 5
z = x + y
resultado = z * 2
teste = 15 pau_a_pau 15
condicao = 10 miudo 20
valor = 7 - 3 + 2
```

**Saída (Relatório de Tokens):**
```
TOKEN                    TIPO                     VALOR              POSICAO
Trem                     PALAVRA_RESERVADA        Trem               L1,C1
cheio                    IDENTIFICADOR            cheio              L1,C6
x                        IDENTIFICADOR            x                  L1,C12
=                        OPERADOR_ATRIBUICAO      =                  L1,C14
10                       NUMERO                   10                 L1,C16
...
valor                    IDENTIFICADOR            valor              L7,C1
=                        OPERADOR_ATRIBUICAO      =                  L7,C7
7                        NUMERO                   7                  L7,C9
-                        OPERADOR_ARITMETICO      -                  L7,C11
3                        NUMERO                   3                  L7,C13
+                        OPERADOR_ARITMETICO      +                  L7,C15
2                        NUMERO                   2                  L7,C17
```

**Estatísticas:**
- IDENTIFICADOR: 14 tokens
- NUMERO: 10 tokens
- OPERADOR_ARITMETICO: 4 tokens
- OPERADOR_ATRIBUICAO: 7 tokens
- PALAVRA_RESERVADA: 2 tokens
- **Total: 37 tokens**

**Grafos Gerados:**
- ✅ `exemplo_teste_automato.png` (102 KB) - Grafo do DFA
- ✅ `exemplo_teste_arvore.png` (393 KB) - Árvore de leitura

---

### 🔍 COMO O DFA FUNCIONA (PASSO A PASSO)

**Entrada:** `Trem x = 10`

| Passo | Char | Estado Atual | Ação | Estado Novo | Lexema | Token Emitido |
|-------|------|--------------|------|-------------|--------|---------------|
| 1 | T | START | LETRA encontrada | ID | T | - |
| 2 | r | ID | LETRA, continua | ID | Tr | - |
| 3 | e | ID | LETRA, continua | ID | Tre | - |
| 4 | m | ID | LETRA, continua | ID | Trem | - |
| 5 | (espaço) | ID | Sem transição | START | - | PALAVRA_RESERVADA:Trem |
| 6 | x | START | LETRA encontrada | ID | x | - |
| 7 | (espaço) | ID | Sem transição | START | - | IDENTIFICADOR:x |
| 8 | = | START | ATRIB | ATRIB_OR_EQ | = | - |
| 9 | (espaço) | ATRIB_OR_EQ | Sem transição | START | - | OPERADOR_ATRIBUICAO:= |
| 10 | 1 | START | DIGITO | NUM | 1 | - |
| 11 | 0 | NUM | DIGITO, continua | NUM | 10 | - |
| 12 | (fim) | NUM | - | - | - | NUMERO:10 |

---

### 📦 ARQUIVOS CRIADOS/MODIFICADOS

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| `analisador_lexico_com_grafo.py` | Principal | Implementação completa do lexer com DFA |
| `demo_analisador.py` | Script | Demonstração interativa de funcionalidades |
| `README_ANALISADOR_LEXICO.md` | Documentação | Guia completo de uso e conceitos |
| `exemplo_teste_automato.png` | Visual | Grafo do autômato finito |
| `exemplo_teste_arvore.png` | Visual | Árvore de tokens por linha |

---

### 🧰 DEPENDÊNCIAS

```bash
pip install networkx matplotlib
```

- **networkx**: Criação e manipulação de grafos
- **matplotlib**: Visualização e salvamento de gráficos em PNG

---

### 💡 CONCEITOS-CHAVE EXPLICADOS

#### **1. Autômato Finito Determinístico (DFA)**
- Máquina de estados que **sempre** segue um único caminho para uma entrada
- Estados e transições pré-definidas
- Determinístico = não há múltiplas escolhas

#### **2. Tabela de Transições**
```python
grafo["START"]["LETRA"] = "ID"  # Se em START e entrada é LETRA → ID
grafo["ID"]["DIGITO"] = "ID"    # Se em ID e entrada é DIGITO → continua em ID
```

#### **3. Lexema**
- Substring sendo construída enquanto muda de estado
- Emitido como token quando transição não existe

#### **4. Classificação de Entrada**
```python
def _classe_char(c):
    if c.isalpha(): return "LETRA"      # a-z, A-Z
    if c.isdigit(): return "DIGITO"     # 0-9
    if c in "<>!": return "REL"         # Operadores relacionais
    return c                             # Retorna o próprio char
```

---

### ✨ CARACTERÍSTICAS ESPECIAIS

✅ **Rastreamento de Posição**: Linha e coluna de cada token  
✅ **Suporte a Números Decimais**: `10.5`, `3.14`, etc.  
✅ **Strings com Aspas**: `"texto"` ou `'texto'`  
✅ **Comentários**: Linhas com `#`  
✅ **Visualização de Grafos**: PNG com NetworkX + Matplotlib  
✅ **Interface Interativa**: Menu de opções para usuário  
✅ **Tratamento de Erros**: Caracteres inválidos relatados  
✅ **Relatório Tabular**: Formato claro com Token, Tipo, Valor, Posição  

---

### 🚀 PRÓXIMOS PASSOS SUGERIDOS

1. **Integrar com Parser Sintático**
   - Usar tokens gerados como entrada para análise sintática
   - Construir AST (Abstract Syntax Tree)

2. **Adaptar para SertaLanguage Completa**
   - Adicionar tokens específicos: `{[`, `]}`, `Uai`, `pau_a_pau`, `miúdo`, etc.
   - Expandir palavras-reservadas

3. **Interface Gráfica (Tkinter)**
   - Integrar visualização de grafos na GUI
   - Seletor de arquivo com FileDialog
   - Previsualizador de tokens em tempo real

4. **Export de Relatórios**
   - JSON com estrutura completa
   - CSV para análise em Excel
   - HTML para visualização web

5. **Otimizações**
   - Usar Regex compiladas para performance
   - Cache de transições frequentes

---

### 📞 RESUMO FINAL

O `analisador_lexico_com_grafo.py` implementa um **analisador léxico profissional** baseado em **autômato finito**, com capacidades de:

- ✅ Tokenização precisa linha a linha
- ✅ Rastreamento de posição (linha, coluna)
- ✅ Visualização do grafo do DFA
- ✅ Visualização em árvore da leitura
- ✅ Entrada flexível (inline ou arquivo)
- ✅ Saída em múltiplos formatos (console, PNG)

Pronto para ser usado como base para compiladores, interpretadores, ou ferramentas de análise de código!

---

**Data de Criação**: 23 de Maio de 2026  
**Versão**: 1.0 Final  
**Status**: ✅ Totalmente Funcional e Testado
