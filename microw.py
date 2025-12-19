import sys
from enum import Enum
from pathlib import Path
import codecs

MAN = """
NOME
    microw - convert data to MicroSIP accounts

USO
    python3 microw.py [OPÇÔES]

DESCRIÇÂO
    Utilitário para conversão de dados tabulares (CSV, TXT) em arquivos de 
    configuração (.ini) para o softphone MicroSIP e variantes.

    Feito por Lúcio Carvalho Almeida, Free Software.

ARGUMENTOS
    --format <string>       Define a ordem das colunas no arquivo de entrada.
                            Use nomes de variáveis (ex: ramal, password) ou
                            '_' para ignorar uma coluna específica.
                            Padrão: "ramal label"
                            Variáveis especiais: 'name', 'label', 'password',
                            'server'

    --input <path>          Caminho do arquivo de origem dos dados.
                            Padrão: "./input.txt"

    --output <path>         Caminho onde o arquivo .ini será gerado.
                            Padrão: "./output.ini"

    --delimiter <sep>       Caractere separador de colunas (aceita '\\t', ' ').
                            Padrão: ","

    --label-pattern <q>     Template para customizar o nome de exibição.
                            Substitui nomes de variáveis pelos seus valores.
                            Ex: "ramal - label (setor)"

    --add-ghost             Se presente, adiciona uma conta de 'Desconectado'
                            como o primeiro perfil da lista.

    --set-template <t>      Fornece o caminho para o arquivo <t> que será
                            usado no lugar de ACCOUNT_TEMPLATE

    --read-encoding <ienc>  Define a codificação de leitura

EXEMPLOS
    1. Formato padrão com separador de ponto e vírgula:
        python3 microw.py --delimiter ";"

    2. Ignorando a 1ª coluna e formatando o nome de exibição:
        python3 microw.py --format "_ ramal label setor" --label-pattern "label [setor]"

    3. Usando um arquivo específico e adicionando conta fantasma:
        python3 microw.py --input lista_vendas.csv --add-ghost

CREDITOS
    Desenvolvido por Lúcio Carvalho Almeida, Open Source.
    Contato em luciocarvalhodev@gmail.com.
"""

ACCOUNT_TEMPLATE = r'''
[Account_]
label=$label
server=$server
proxy=$server
domain=$server
username=$ramal
password=$password
authID=$ramal
displayName=
dialingPrefix=
dialPlan=
hideCID=0
voicemailNumber=
transport=udp
publicAddr=
SRTP=
registerRefresh=300
keepAlive=15
publish=0
ICE=0
allowRewrite=0
disableSessionTimer=0
'''

GHOST_TEMPLATE = r'''
[Account_]
label=Desconectado
server=0.0.0.0
proxy=0.0.0.0
domain=0.0.0.0
username=0000
password=1234
authID=0000
'''

class SchemaValue(Enum):
    Argument = 1
    Bool = 2

class Config:
    def __init__(self):
        self.config = {
            "format": {
                "default": "ramal label",
                "schema": SchemaValue.Argument,
                "value": None
            },
            "input": {
                "default": "./input.txt",
                "schema": SchemaValue.Argument,
                "value": None
            },
            "add-ghost": {
                "default": False,
                "schema": SchemaValue.Bool,
                "value": None
            },
            "delimiter": {
                "default": ",",
                "schema": SchemaValue.Argument,
                "value": None
            },
            "output": {
                "default": "./output.ini",
                "schema": SchemaValue.Argument,
                "value": None
            },
            "label-pattern": {
                "default": "label",
                "schema": SchemaValue.Argument,
                "value": None
            },
            "help": {
                "default": None,
                "schema": SchemaValue.Bool,
                "value": None
            },
            "set-template": {
                "default": None,
                "schema": SchemaValue.Argument,
                "value": None
            }
        }
    
    def _validate_setting(self, setting):
        if not setting in self.config:
            raise ValueError(f"'{setting}' is not a valid option.")
    
    def get(self, setting):
        self._validate_setting(setting)
        return self.config[setting]["value"] or self.config[setting]["default"]

    def set(self, setting, value):
        self._validate_setting(setting)
        self.config[setting]["value"] = value
    
    def schema(self, setting):
        self._validate_setting(setting)
        return self.config[setting]["schema"]

config = Config()

def main():
    # Faz o parse manual das flags e argumentos
    args = sys.argv[1:]
    while len(args):
        argument = args.pop(0)
        if argument[:2] == "--":
            argument = argument[2:]
        
        if argument == "help":
            print(MAN)
            return
        
        if config.schema(argument) == SchemaValue.Argument:
            config.set(argument, codecs.decode(args.pop(0), "unicode_escape"))
        else:
            config.set(argument, not config.get(argument))

    output_file = Path(config.get("output"))
    input_file = Path(config.get("input"))
    input_lines = [line.strip() for line in input_file.open("r", encoding="utf-8").readlines()]

    accounts_settings = []
    format_vars = config.get("format").split(" ")
    label_pattern = config.get("label-pattern")

    for line in input_lines:
        if not line: continue
        
        data = [field.strip() for field in line.split(config.get("delimiter"))]
        account_dict = {}

        # Mapeia os dados ignorando o caractere '_'
        for i in range(min(len(data), len(format_vars))):
            var_name = format_vars[i]
            if var_name != "_":
                account_dict[var_name] = data[i]
        
        # Customização do $label
        if label_pattern:
            pattern_parts = label_pattern.split(" ")

            # Se a parte for uma variável conhecida, substitui pelo valor
            new_label = " ".join([account_dict.get(name, name) for name in pattern_parts])
            account_dict["label"] = new_label
        
        accounts_settings.append(account_dict)

    result = ""

    if config.get("add-ghost"):
        result += GHOST_TEMPLATE
    
    current_account_template = ACCOUNT_TEMPLATE

    if not config.get("set-template") is None:
        current_account_template = Path(config.get("set-template")).read_text(encoding="utf-8")

    for account in accounts_settings:
        new_entry = current_account_template
        # Substitui todas as variáveis encontradas
        for var_name, value in account.items():
            new_entry = new_entry.replace("$" + var_name, str(value))
        
        result += new_entry.strip() + "\n"

    result = result.strip()

    # Numeração sequencial das contas [Account1], [Account2]...
    id = 1
    while "Account_" in result:
        result = result.replace("Account_", f"Account{id}", 1)
        id += 1

    output_file.write_text(result, encoding="utf-8")
    print(f"Sucesso: {id-1} contas criadas em '{output_file}'.")

main()