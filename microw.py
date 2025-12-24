import sys
from enum import Enum
from pathlib import Path
import codecs
import re
from textwrap import wrap

MAN_DESCRIPTION = """
NOME
microw - convert data to MicroSIP accounts

USO
python3 microw.py [OPÇÔES]

DESCRIÇÂO
Utilitário para conversão de dados tabulares (CSV, TXT) em arquivos de 
configuração (.ini) para o softphone MicroSIP e variantes.

Feito por Lúcio Carvalho Almeida, Free Software."""

MAN_FOOTER = """
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

class Flags(Enum):
    format = "format"
    input = "input"
    add_ghost = "add-ghost"
    delimiter = "delimiter"
    output = "output"
    label_pattern = "label-pattern"
    help = "help"
    set_template = "set-template"
    read_encoding = "read-encoding"
    write_encoding = "write-encoding"
    sort_by = "sort-by"
    sort = "sort"

    @classmethod
    def from_str(cls, name: str):
        normalized_flag_name = name.replace("-", "_")
        if not normalized_flag_name in cls.__members__:
            error_string = f"O argumento '--{name}' não corresponde a uma flag válida."
            raise ValueError(error_string)    
        return cls[normalized_flag_name]
    
    def to_str(self):
        return self._value_

# Quantidade de argumentos esperados
class FlagSchema(Enum):
    NoArgument = 0
    Argument = 1

# Os métodos dessa classe recebem instancias de Flags
class Config:
    def __init__(self):
        self.flags = {}
        self.define_flag(Flags.format,FlagSchema.Argument, "ramal label", """Define a ordem das colunas no arquivo de entrada. Use nomes de variáveis (ex: ramal, password) ou '_' para ignorar uma coluna específica.""")
        self.define_flag(Flags.input, FlagSchema.Argument, "./input.txt", """Caminho do arquivo de origem dos dados.""")
        self.define_flag(Flags.delimiter, FlagSchema.Argument, ",", """Define qual string sera considerada como seprador das colunas de cada linha do input.""")
        self.define_flag(Flags.add_ghost, FlagSchema.NoArgument, False, """Se presente, adiciona uma conta de 'Desconectado' como o primeiro perfil da lista.""")
        self.define_flag(Flags.output, FlagSchema.Argument, "./output.ini", """Caminho onde o arquivo .ini será gerado.""")
        self.define_flag(Flags.label_pattern, FlagSchema.Argument, "label", """Template para customizar o nome de exibição. Substitui nomes de variáveis pelos seus valores.""")
        self.define_flag(Flags.help, FlagSchema.NoArgument, False, """Exibe o manual.""")
        self.define_flag(Flags.set_template, FlagSchema.Argument, None, """Forcene o caminho para um arquivo que servira como template.""")
        self.define_flag(Flags.read_encoding, FlagSchema.Argument, "utf-8", "Codificação do arquivo lido por '--input'")
        self.define_flag(Flags.write_encoding, FlagSchema.Argument, "utf-8", "Codificação do arquivos gerados.")
        self.define_flag(Flags.sort, FlagSchema.NoArgument, True, """Ordena as contas no arquivo final.""")
        self.define_flag(Flags.sort_by, FlagSchema.Argument, "ramal", """Define qual a coluna usada para ordenação.""")

    def generate_flags_man(self):
        res = [MAN_DESCRIPTION]
        for flag in Flags:
            res.append(self.flag_man(flag))

        res.append(MAN_FOOTER)

        return "\n".join(res)

    def flag_man(self, flag: Flags):
        ident = "    " * 5

        lines = wrap(self.flags[flag]["man"], 60)
        lines[0] = (f"--{flag.to_str()}{ident}"[0:len(ident)] + lines[0])

        for i in range(len(lines)-1):
            lines[i+1] = ident + lines[i+1]
        
        return "\n".join(lines)

    def load_args(self, args: list[str]):
        while len(args):
            argument = args.pop(0)
            if argument[:2] == "--":
                argument = argument[2:]
            
            flag = Flags.from_str(argument)
            
            if self.schema(flag) == FlagSchema.Argument:
                if len(args) == 0:
                    msg_error = f"Flag '--{argument}' exige um argumento."
                    raise ValueError(msg_error)
                self.set(flag, codecs.decode(args.pop(0), "unicode_escape"))
            else:
                self.set(flag, not self.getDefault(flag))
    
    def define_flag(self, flag: Flags, schema: FlagSchema, default, man: str):
        self.flags[flag] = {
            "schema": schema,
            "default": default,
            "man": man
        }
    
    def _validate_setting(self, setting: Flags):
        if not isinstance(setting, Flags):
            raise ValueError(f"'{setting}' is not a valid flag.")

        return setting.value
    
    def get(self, setting):
        self._validate_setting(setting)
        return self.flags[setting].get("value", self.flags[setting]["default"])
    
    def getDefault(self, setting):
        self._validate_setting(setting)
        return self.flags[setting]["default"]

    def set(self, setting, value):
        self._validate_setting(setting)
        self.flags[setting]["value"] = value
    
    def schema(self, setting):
        self._validate_setting(setting)
        return self.flags[setting]["schema"]


def main():
    config = Config()
    config.load_args(sys.argv[1:])
    
    if config.get(Flags.help):
        print(config.generate_flags_man())
        return

    output_file = Path(config.get(Flags.output))
    input_file = Path(config.get(Flags.input))
    if not input_file.exists():
        error_msg = f"Arquivo de input especificado '{input_file.name}' não encontrado."
        raise ValueError(error_msg)
    input_lines = [line.strip() for line in input_file.open("r", encoding=config.get(Flags.read_encoding)).readlines()]

    accounts_settings = []
    format_vars = config.get(Flags.format).split(" ")
    label_pattern = config.get(Flags.label_pattern)

    for line in input_lines:
        if not line: continue
        
        data = [field.strip() for field in line.split(config.get(Flags.delimiter))]
        account_dict = {}

        # Mapeia os dados ignorando o caractere '_'
        for i in range(min(len(data), len(format_vars))):
            var_name = format_vars[i]
            if var_name != "_":
                account_dict[var_name] = data[i]
        
        # Customização do $label
        formated_pattern = label_pattern
        for pattern_part in re.finditer(r"[a-zA-Z]+", label_pattern):
            pattern = pattern_part.group()
            if pattern in format_vars:
                formated_pattern = formated_pattern.replace(pattern, data[format_vars.index(pattern)]) 

        
        account_dict["label"] = formated_pattern
        accounts_settings.append(account_dict)
    
    if config.get(Flags.sort) : accounts_settings.sort(key=lambda account : account[config.get(Flags.sort_by)])

    result = ""

    if config.get(Flags.add_ghost):
        result += GHOST_TEMPLATE
    
    current_account_template = ACCOUNT_TEMPLATE

    if not config.get(Flags.set_template) is None:
        current_account_template = Path(config.get(Flags.set_template)).read_text(encoding=config.get(Flags.read_encoding))

    for account in accounts_settings:
        new_entry = current_account_template
        for var_name, value in account.items():
            new_entry = new_entry.replace("$" + var_name, str(value))
        
        result += new_entry.strip() + "\n"

    result = result.strip()

    id = 1
    while "Account_" in result:
        result = result.replace("Account_", f"Account{id}", 1)
        id += 1

    output_file.write_text(result, encoding=config.get(Flags.write_encoding))
    print(f"Sucesso: {id-1} contas criadas em '{output_file}'.")

main()