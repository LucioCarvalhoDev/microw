# Microw

**Microw** é um utilitário de linha de comando (CLI) desenvolvido em Python para automatizar a conversão de dados tabulares (como arquivos CSV ou TXT) em arquivos de configuração `.ini` compatíveis com o softphone **MicroSIP** e seus derivados.

Esta ferramenta é ideal para administradores de sistemas VoIP, suporte técnico e desenvolvedores que precisam realizar o provisionamento em massa de ramais de forma rápida e precisa.

## Funcionalidades

* **Mapeamento Flexível:** Define a ordem das colunas do seu arquivo de entrada via linha de comando.
* **Templates Customizáveis:** Permite o uso de modelos de conta personalizados para diferentes cenários de rede.
* **Padrões de Label:** Gere nomes de exibição (DisplayName) dinâmicos baseados nos dados de entrada.
* **Conta Ghost:** Opção para adicionar um perfil "Desconectado" como primeira conta da lista.
* **Suporte a Delimitadores:** Funciona com vírgulas, tabs (`\t`), pontos e vírgulas, etc.

## Como Usar

### Pré-requisitos

* Python 3.x instalado.

### Instalação

Basta clonar o repositório ou baixar o arquivo `microw.py`:

```bash
git clone https://github.com/LucioCarvalhoDev/microw.git
cd microw
```

### Execução Básica

Supondo que você tenha um arquivo `seus_dados.csv` com o formato `ramal,label`:

```bash
python3 microw.py --input seus_dados.csv --output accounts.ini
```

---

## Referência de Argumentos

| Argumento | Padrão | Descrição |
| --- | --- | --- |
| `--format` | `"ramal label"` | Ordem das colunas (use `_` para ignorar colunas). |
| `--input` | `./input.txt` | Caminho do arquivo de origem. |
| `--output` | `./output.ini` | Caminho do arquivo `.ini` gerado. |
| `--delimiter` | `,` | Caractere separador de colunas. |
| `--label-pattern` | `label` | Template para o nome de exibição (ex: `"ramal - label"`). |
| `--add-ghost` | `False` | Adiciona conta de 'Desconectado' no topo. |
| `--set-template` | `None` | Caminho para um arquivo de template de conta customizado. |

---

## Exemplos de Uso

### 1. Formato CSV com Ponto e Vírgula

Se o seu arquivo segue o padrão `ID;Ramal;Nome;Setor` e você quer ignorar o ID:

```bash
python3 microw.py --delimiter ";" --format "_ ramal label setor"

```

### 2. Customizando o Nome de Exibição

Para que no MicroSIP o nome apareça como `Ramal | Nome (Setor)`:

```bash
python3 microw.py --format "ramal label setor" --label-pattern "ramal | label (setor)"

```

### 3. Usando um Template de Conta Específico

Se você precisa de configurações de transporte (TLS/TCP) ou portas diferentes, crie um arquivo de template e aponte-o:

```bash
python3 microw.py --set-template meu_modelo.txt --input ramais.txt

```

---

## Licença e Créditos

Desenvolvido por **Lúcio Carvalho Almeida**.

Este projeto é **Software Livre** (Open Source).

**Contato:** [luciocarvalhodev@gmail.com](mailto:luciocarvalhodev@gmail.com)

---

Sinta-se à vontade para contribuir com Pull Requests!

---
