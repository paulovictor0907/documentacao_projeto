import os
import binascii
import requests


output_folder = "diagrams_hex"
os.makedirs(output_folder, exist_ok=True)


def encode_plantuml_hex(data):
    
    hex_encoded = binascii.hexlify(data.encode('utf-8')).decode('utf-8')
    return "~h" + hex_encoded


def generate_uml_url_hex(diagram_text):
    base_url = "http://www.plantuml.com/plantuml/png/"
    encoded_text = encode_plantuml_hex(diagram_text)
    return base_url + encoded_text


def save_diagram_hex(diagram_text, filename):
    url = generate_uml_url_hex(diagram_text)
    try:
        response = requests.get(url)
        response.raise_for_status()
        filepath = os.path.join(output_folder, filename)
        with open(filepath, "wb") as file:
            file.write(response.content)
        return f"Diagrama salvo como: {filepath}"
    except Exception as e:
        return f"Erro ao gerar o diagrama {filename}: {e}"


diagrams = {
    "component_diagram": """
@startuml
package "Sistema de Méritos" {
    component "Cadastro de Usuários" {
        [Aluno] --> [Cadastro de Usuários]
        [Professor] --> [Cadastro de Usuários]
        [Empresa Parceira] --> [Cadastro de Usuários]
    }

    component "Distribuição de Moedas" {
        [Professor] --> [Distribuição de Moedas]
        [Aluno] <-- [Distribuição de Moedas]
    }

    component "Notificação" {
        [Aluno] <-- [Notificação]
        [Distribuição de Moedas] --> [Notificação]
    }

    component "Consulta de Saldo e Extrato" {
        [Aluno] --> [Consulta de Saldo e Extrato]
        [Professor] --> [Consulta de Saldo e Extrato]
    }

    component "Troca de Vantagens" {
        [Aluno] --> [Troca de Vantagens]
        [Empresa Parceira] <-- [Troca de Vantagens]
    }

    component "Autenticação" {
        [Aluno] --> [Autenticação]
        [Professor] --> [Autenticação]
        [Empresa Parceira] --> [Autenticação]
    }

    [Cadastro de Usuários] --> [Autenticação]
    [Distribuição de Moedas] --> [Consulta de Saldo e Extrato]
    [Troca de Vantagens] --> [Consulta de Saldo e Extrato]
}
@enduml
    """,
    "implantation_diagram": """
    @startuml
node "Servidor Web" {
    component "Frontend" {
        [Interface Usuário]
    }
    component "Backend" {
        [API REST]
    }
}

node "Servidor de Banco de Dados" {
    database "Banco de Dados" {
        [Tabelas de Usuários]
        [Tabelas de Transações]
        [Tabelas de Moedas]
    }
}

node "Servidor de Email" {
    [Serviço de Notificação]
}

[Frontend] --> [Backend]
[Backend] --> [Banco de Dados]
[Backend] --> [Serviço de Notificação]

    @enduml
    """,
    "class_diagram": """
    @startuml
class Usuario {
    +id: int
    +nome: string
    +email: string
    +senha: string
    +cpf: string
    +login(): void
}

class Aluno {
    +instituicao: string
    +curso: string
    +moedas: int
    +consultarExtrato(): void
    +trocarMoedas(): void
}

class Professor {
    +departamento: string
    +distribuirMoedas(aluno: Aluno, quantidade: int, motivo: string): void
    +consultarExtrato(): void
}

class EmpresaParceira {
    +nome: string
    +vantagens: string[]
    +cadastrarVantagem(descricao: string, foto: string): void
    +enviarCodigoResgate(aluno: Aluno): void
}

class Moeda {
    +quantidade: int
    +distribuir(quantidade: int): void
}

class Notificacao {
    +mensagem: string
    +enviarNotificacao(usuario: Usuario): void
}

Usuario <|-- Aluno
Usuario <|-- Professor
Usuario <|-- EmpresaParceira

Aluno "1" -- "0..*" Moeda : possui
Professor "1" -- "0..*" Moeda : distribui
Professor "1" -- "0..*" Notificacao : envia
EmpresaParceira "1" -- "0..*" Notificacao : envia

@enduml
""",
    "state_diagram": """@startuml
[*] --> Inativo

state Inativo {
    [*] --> Cadastro
    Cadastro --> Ativo : Cadastro Completo
}

state Ativo {
    [*] --> ConsultandoExtrato
    [*] --> RecebendoMoedas
    [*] --> TrocandoMoedas

    ConsultandoExtrato --> ConsultandoExtrato : Solicitação de Extrato
    RecebendoMoedas --> RecebendoMoedas : Moedas Distribuídas
    TrocandoMoedas --> TrocandoMoedas : Solicitação de Troca

    RecebendoMoedas --> ConsultandoExtrato : Ver Saldo
    TrocandoMoedas --> ConsultandoExtrato : Ver Saldo
    ConsultandoExtrato --> RecebendoMoedas : Receber Moedas
    ConsultandoExtrato --> TrocandoMoedas : Trocar Moedas
}

state DistribuindoMoedas {
    [*] --> SelecionandoAluno
    SelecionandoAluno --> ConfirmandoDistribuicao : Aluno Selecionado
    ConfirmandoDistribuicao --> DistribuicaoConcluida : Moedas Distribuídas
    DistribuicaoConcluida --> [*]
}

Ativo --> DistribuindoMoedas : Distribuir Moedas
DistribuindoMoedas --> Ativo : Moeda Distribuída
@enduml
""",
"sequence_diagram": """@startuml
@startuml
actor Professor
actor Aluno
participant "Sistema de Mérito" as Sistema
participant "API de Moedas" as API_Moedas
participant "Notificação" as Notificacao

Professor -> Sistema : Solicita Distribuição de Moedas(aluno, quantidade, motivo)
Sistema -> API_Moedas : Validar Quantidade de Moedas
API_Moedas -> Sistema : Quantidade de Moedas Validada
Sistema -> Aluno : Atualiza Saldo de Moedas
Sistema -> Notificacao : Envia Notificação ao Aluno
Notificacao -> Aluno : Notificação Recebida
Sistema -> Professor : Confirmação de Distribuição Concluída

@enduml
""",
}


results = {}
for name, text in diagrams.items():
    results[name] = save_diagram_hex(text, f"{name}_hex.png")


print(results)
