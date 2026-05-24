# 📖 ÍNDICE DO PROJETO: Analisador Léxico com DFA e Visualização de Grafos

---

## 📁 Estrutura de Arquivos do Projeto

```
Analisador_Lexico_Linguagem/
├── 📄 DOCUMENTAÇÃO
│   ├── INDEX.md                        ← Você está aqui!
│   ├── README_ANALISADOR_LEXICO.md     ← Guia completo de uso
│   ├── RESUMO_IMPLEMENTACAO.md         ← Conceitos e evolução
│   └── README.md (original)            ← Documentação do projeto original
│
├── 🚀 ARQUIVOS EXECUTÁVEIS
│   ├── analisador_lexico_com_grafo.py  ← PRINCIPAL - Lexer com DFA
│   ├── demo_analisador.py              ← Demonstração automática
│   ├── exemplos_praticos.py            ← Menu com 7 exemplos interativos
│   ├── sertaLanguage.py                ← Lexer anterior (biblioteca SLY)
│   └── main.py                         ← Exemplo de calculadora SLY
│
├── 📊 GRAFOS GERADOS (PNG)
│   ├── exemplo_teste_automato.png      ← Grafo do DFA
│   └── exemplo_teste_arvore.png        ← Árvore de tokens por linha
│
├── 📝 ARQUIVOS DE TESTE
│   ├── exemplo_teste.txt               ← Código para testar lexer
│   ├── codigo_valido.txt               ← Teste de SertaLanguage
│   ├── codigo_invalido.txt             ← Teste de erro
│   └── testesertalanguage.txt          ← Outro arquivo de teste
│
└── 🔧 AMBIENTE
    └── venv/                           ← Ambiente virtual Python (não incluído)
        └── Scripts/python.exe          ← Interpretador Python 3.14
```

---

## 📋 Descrição Detalhada dos Arquivos

### 🎯 ARQUIVOS PRINCIPAIS (use estes!)

#### **1. `analisador_lexico_com_grafo.py`** (16 KB)
**STATUS:** ✅ PRINCIPAL - VERSÃO FINAL

O arquivo mais importante! Implementação completa do lexer com:
- Classe `Token` (dataclass)
- Classe `AnalisadorLexicoComGrafo` com DFA
- Métodos de análise (inline ou arquivo)
- Construção de grafos (automato + arvore)
- Visualização com Matplotlib/NetworkX
- Relatório tabular formatado

**Como usar:**
```bash
.\venv\Scripts\python.exe analisador_lexico_com_grafo.py
```

Solicitará:
1. Caminho do arquivo
2. Se quer visualizar grafos
3. Se quer salvar como PNG

**Output:**
- Grafo de transições (texto)
- Relatório de tokens (tabela)
- `*_automato.png` - Grafo do DFA
- `*_arvore.png` - Árvore de leitura

---

#### **2. `demo_analisador.py`** (3,8 KB)
**STATUS:** ✅ DEMONSTRAÇÃO

Script que executa automaticamente 3 demos:
1. Análise de código inline
2. Análise de arquivo
3. Exibição do grafo do autômato

**Como usar:**
```bash
.\venv\Scripts\python.exe demo_analisador.py
```

Sem entrada necessária. Executa e exibe resultado completo.

**Ideal para:** Ver tudo funcionando em uma execução
**Output:** Tabelas formatadas com estatísticas

---

#### **3. `exemplos_praticos.py`** (9 KB)
**STATUS:** ✅ MENU INTERATIVO

Menu com 7 exemplos práticos da API:
1. Uso Básico
2. Múltiplas Linhas
3. Análise de Arquivo
4. Filtrar Tokens por Tipo
5. Verificar Posição de Tokens
6. Gerar Estatísticas
7. Construir Grafo do Autômato

**Como usar:**
```bash
.\venv\Scripts\python.exe exemplos_praticos.py
```

Menu interativo permite selecionar exemplos um por um ou executar todos.

**Ideal para:** Aprender a usar a API com exemplos práticos
**Output:** Demonstra cada função e capacidade

---

### 📚 DOCUMENTAÇÃO

#### **4. `README_ANALISADOR_LEXICO.md`** (10 KB)
**Conteúdo:**
- Visão geral completa
- Estrutura do código
- Fluxo de tokenização (com exemplo)
- Visualização de grafos
- Como usar o programa
- Tipos de tokens reconhecidos
- Comparação SLY vs DFA Manual

**Leia quando:** Quer entender como funciona
**Indicado para:** Estudos e compreensão profunda

---

#### **5. `RESUMO_IMPLEMENTACAO.md`** (14,6 KB)
**Conteúdo:**
- O que foi implementado
- Evolução do código (5 estágios)
- Fluxo de execução completo (diagrama)
- Exemplo real de execução
- Passo a passo de como o DFA funciona
- Conceitos-chave explicados
- Características especiais

**Leia quando:** Quer saber o que foi feito e por quê
**Indicado para:** Visão de projeto e metodologia

---

#### **6. `INDEX.md`** (Este arquivo)
**Conteúdo:**
- Mapa completo do projeto
- Descrição de cada arquivo
- Como escolher qual usar
- Quick start
- Guia de resolução de problemas

---

### 🧪 ARQUIVOS DE TESTE

#### **7. `exemplo_teste.txt`** (0,1 KB)
Arquivo com código de teste padrão:
```
Trem cheio x = 10
Trem quebrado y = 5
z = x + y
resultado = z * 2
teste = 15 pau_a_pau 15
condicao = 10 miudo 20
valor = 7 - 3 + 2
```

Usado por padrão na demonstração.

---

#### **8. `codigo_valido.txt`** (0,1 KB)
Arquivo com código válido de teste.

---

#### **9. `codigo_invalido.txt`** (0,0 KB)
Arquivo com código inválido para teste de erro.

---

### 🎨 GRAFOS GERADOS

#### **10. `exemplo_teste_automato.png`** (102 KB)
Visualização do **Autômato Finito Determinístico:**
- Nós = Estados (START, ID, NUM, etc.)
- Setas = Transições (com entrada)
- Cores: Nós verdes, setas verdes escuras

**Gerado por:** `construir_grafo_automato()`

---

#### **11. `exemplo_teste_arvore.png`** (393 KB)
Visualização da **Árvore de Leitura:**
- Raiz = ARQUIVO
- Branches = Linhas (LINHA_1, LINHA_2, etc.)
- Folhas = Tokens (T1:PALAVRA_RESERVADA:Trem, etc.)

**Gerado por:** `construir_arvore_tokens()`

---

### 🏛️ ARQUIVOS ANTERIORES (Referência)

#### **12. `sertaLanguage.py`** (11,6 KB)
Implementação anterior usando biblioteca **SLY** (Python Lex-Yacc).

**Diferenças:**
- SLY: Declarativo, fácil, menos controle
- DFA Manual: Imperativo, mais controle, entende-se o algoritmo

**Não use para novo código.** Mantido para referência.

---

#### **13. `main.py`** (2 KB)
Exemplo de calculadora da biblioteca SLY (referência).

**Não diretamente relacionado ao projeto.**

---

#### **14. `testesertalanguage.txt`** (0,3 KB)
Arquivo de teste antigo.

---

## 🚀 QUICK START

### Opção 1: Usar o Analisador (recomendado primeiro)
```bash
.\venv\Scripts\python.exe analisador_lexico_com_grafo.py
```
- Digite: `exemplo_teste.txt`
- Digite: `s` (sim para grafos)
- Digite: `s` (sim para salvar PNG)
- Digite: `exemplo_teste` (prefixo)

**Resultado:** Tokens exibidos + 2 PNG gerados

---

### Opção 2: Ver Demonstração Automática
```bash
.\venv\Scripts\python.exe demo_analisador.py
```
**Resultado:** 3 demos executadas automaticamente

---

### Opção 3: Exemplos Práticos Interativos
```bash
.\venv\Scripts\python.exe exemplos_praticos.py
```
**Resultado:** Menu para escolher 7 exemplos

---

### Opção 4: Entender o Conceito
1. Leia `README_ANALISADOR_LEXICO.md` (conceitos gerais)
2. Leia `RESUMO_IMPLEMENTACAO.md` (detalhes técnicos)
3. Execute `exemplos_praticos.py` (ver na prática)

---

## 📊 COMPARAÇÃO: QUAL USAR?

| Necessidade | Use | Como |
|-------------|-----|------|
| Ver funcionando rápido | `demo_analisador.py` | Executa direto |
| Trabalhar com arquivo | `analisador_lexico_com_grafo.py` | Menu interativo |
| Aprender API | `exemplos_praticos.py` | Menu + 7 exemplos |
| Entender conceito | `README_ANALISADOR_LEXICO.md` | Leitura |
| Ver evolução | `RESUMO_IMPLEMENTACAO.md` | Leitura |
| Integrar em código | Importe `analisador_lexico_com_grafo.py` | `from analisador_lexico_com_grafo import *` |

---

## 🔧 RESOLUÇÃO DE PROBLEMAS

### Problema: "ModuleNotFoundError: No module named 'networkx'"
**Solução:**
```bash
.\venv\Scripts\python.exe -m pip install networkx matplotlib
```

---

### Problema: Grafo não abre na tela
**Porque:** Sem display gráfico (terminal sem GUI)
**Solução:** Escolha "s" para salvar como PNG (automático)

---

### Problema: Arquivo não encontrado
**Causa:** Caminho incorreto ou arquivo em outra pasta
**Solução:** Forneça caminho completo ou coloque arquivo na pasta do projeto

---

### Problema: Arquivo .txt vazio
**Porque:** Exemplos de teste podem estar vazios
**Solução:** Crie novo arquivo com conteúdo válido

---

## 📈 ROADMAP FUTURO

### Curto Prazo (Próximas versões)
- [ ] Integração com parser sintático
- [ ] Suporte completo a SertaLanguage ({[, ]}, Uai, etc.)
- [ ] Exportação JSON/CSV

### Médio Prazo
- [ ] Geração de AST
- [ ] Interface Tkinter integrada
- [ ] VSCode Extension

### Longo Prazo  
- [ ] Interpretador completo
- [ ] IDE em web browser
- [ ] Suporte múltiplas linguagens

---

## 💡 APRENDIZADO RECOMENDADO

### Se você NÃO sabe como funciona Lexer:
1. Leia `README_ANALISADOR_LEXICO.md` - Conceitos
2. Execute `demo_analisador.py` - Ver funcionando
3. Execute `exemplos_praticos.py` - Exemplos práticos

### Se você quer USAR o Lexer:
1. Execute `analisador_lexico_com_grafo.py` - Interativo
2. Ou importe em seu código:
   ```python
   from analisador_lexico_com_grafo import AnalisadorLexicoComGrafo
   
   lexer = AnalisadorLexicoComGrafo()
   tokens = lexer.analisar("seu código aqui")
   ```

### Se você quer ENTENDER o algoritmo:
1. Leia `RESUMO_IMPLEMENTACAO.md` - Visão completa
2. Abra `analisador_lexico_com_grafo.py` - Estude o código
3. Compare com `sertaLanguage.py` - Veja diferença com SLY

---

## 📞 SUPORTE

**Documentação:** Leia `README_ANALISADOR_LEXICO.md`

**Exemplos:** Execute `exemplos_praticos.py`

**Conceitos:** Leia `RESUMO_IMPLEMENTACAO.md`

**Bugs:** Se encontrar erro, execute `demo_analisador.py` para validar

---

## ✅ STATUS DO PROJETO

| Componente | Status | Versão |
|------------|--------|--------|
| Lexer DFA | ✅ Completo | 1.0 |
| Visualização | ✅ Completo | 1.0 |
| Documentação | ✅ Completo | 1.0 |
| Exemplos | ✅ Completo | 1.0 |
| Testes | ✅ Validado | 1.0 |

**Pronto para produção!**

---

## 📅 Timeline

- **23 de Maio 2026**: Versão 1.0 Final
  - ✅ Implementação completa do DFA
  - ✅ Visualização de grafos com NetworkX
  - ✅ Leitura de arquivo com input do usuário
  - ✅ Documentação completa
  - ✅ Exemplos práticos e demo
  - ✅ Validação e testes

---

**Última atualização: 23 de Maio de 2026**  
**Versão: 1.0 Final**  
**Status: ✅ Pronto para uso**

---

### 🎯 Próximo Passo

Escolha uma das opções abaixo:

1. **Quer ver funcionando rápido?**
   ```bash
   .\venv\Scripts\python.exe demo_analisador.py
   ```

2. **Quer aprender passo a passo?**
   ```bash
   .\venv\Scripts\python.exe exemplos_praticos.py
   ```

3. **Quer usar com seu arquivo?**
   ```bash
   .\venv\Scripts\python.exe analisador_lexico_com_grafo.py
   ```

**Bom trabalho! 🚀**
