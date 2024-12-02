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



"comunication_diagram": """@startuml
    actor Aluno as A
    actor Professor as P
    actor EmpresaParceira as E
    actor SistemaAutenticacao as SA

    control Sistema as S
    boundary BancoDeDados as BD

    A -> SA : Realizar login
    SA -> BD : Validar credenciais
    BD --> SA : Credenciais válidas/ inválidas
    SA --> A : Acesso permitido/negado

    A -> S : Realizar cadastro
    S -> BD : Salvar dados do aluno
    BD --> S : Confirmação do cadastro
    S --> A : Cadastro realizado

    P -> SA : Realizar login
    SA -> BD : Validar credenciais
    BD --> SA : Credenciais válidas/ inválidas
    SA --> P : Acesso permitido/negado

    P -> S : Enviar moedas para aluno
    S -> BD : Verificar saldo de moedas
    BD --> S : Saldo suficiente/insuficiente
    S -> A : Notificar por email
    S -> BD : Registrar transação
    S --> P : Transação realizada/negada

    A -> S : Consultar extrato
    S -> BD : Buscar dados de transações
    BD --> S : Lista de transações
    S --> A : Retornar extrato

    E -> S : Cadastrar vantagem
    S -> BD : Salvar dados da vantagem
    BD --> S : Confirmação do cadastro
    S --> E : Cadastro realizado

    A -> S : Trocar moedas por vantagem
    S -> BD : Verificar saldo e descontar moedas
    BD --> S : Saldo suficiente/insuficiente
    S -> A : Enviar email com cupom
    S -> E : Notificar parceiro com código de troca
    S -> BD : Registrar transação
    S --> A : Confirmação da troca
@enduml""",



"state_diagram": """@startuml
@startuml
[*] --> SistemaNaoAutenticado

state SistemaNaoAutenticado {
    [*] --> TelaLogin
    TelaLogin --> SistemaAutenticado : Credenciais válidas
    TelaLogin --> FalhaLogin : Credenciais inválidas
    FalhaLogin --> TelaLogin : Tentar novamente
}

state SistemaAutenticado {
    [*] --> MenuPrincipal
    
    state MenuPrincipal {
        [*] --> AcessarPerfil
        AcessarPerfil --> ConsultarSaldo : Aluno ou Professor
        AcessarPerfil --> ConsultarExtrato : Aluno ou Professor
        
        AcessarPerfil --> TrocarMoedas : Aluno
        TrocarMoedas --> EscolherVantagem : Selecionar item
        EscolherVantagem --> ConfirmarTroca : Saldo suficiente
        ConfirmarTroca --> MenuPrincipal : Troca realizada
        EscolherVantagem --> TrocaCancelada : Saldo insuficiente
        
        AcessarPerfil --> EnviarMoedas : Professor
        EnviarMoedas --> ConfirmarEnvio : Saldo suficiente
        ConfirmarEnvio --> MenuPrincipal : Transação concluída
        EnviarMoedas --> EnvioCancelado : Saldo insuficiente

        AcessarPerfil --> CadastrarVantagem : EmpresaParceira
        CadastrarVantagem --> ConfirmarCadastro : Dados válidos
        ConfirmarCadastro --> MenuPrincipal : Cadastro realizado
        CadastrarVantagem --> CadastroCancelado : Dados inválidos
    }
    
    MenuPrincipal --> SistemaNaoAutenticado : Logout
}

[*] --> Finalizado : Fim da interação
@enduml""",


"container_diagram": """@startuml
title Diagrama de Contêineres (Nível 2)

node "Sistema de Moeda Estudantil" {
    component Frontend as FE {
        [React: Portal web para Alunos, Professores e Empresas Parceiras]
    }

    component Backend as BE {
        [SpringBoot: Processamento de regras de negócio e API REST]
    }

    database "Banco de Dados" as DB {
        [PostgreSQL: Dados de usuários, transações e vantagens]
    }

    BE --> DB : Consultas e atualizações de dados
    FE --> BE : Requisições HTTP (JSON)

    component EmailService as ES {
        [Serviço de Email: Notificação de transações e cupons]
    }
    BE --> ES : Envio de emails
}

actor Aluno as A
actor Professor as P
actor EmpresaParceira as E
actor Administrador as Admin

A --> FE : Cadastro, envio e troca de moedas
P --> FE : Consulta e envio de moedas
E --> FE : Cadastro de vantagens
Admin --> FE : Gerenciamento do sistema
@enduml""",


"context_diagram": """@startuml
title Diagrama de Contexto (Nível 1)

actor Aluno as Aluno
actor Professor as Professor
actor EmpresaParceira as EmpresaParceira
actor Administrador as Admin

node "Sistema de Moeda Estudantil" {
    rectangle Backend as Backend {
        [API Rest]
        [Banco de Dados]
    }
    rectangle Frontend as Frontend {
        [Portal Web]
    }
}

Aluno --> Frontend : Acessar sistema (Login)
Professor --> Frontend : Acessar sistema (Login)
EmpresaParceira --> Frontend : Acessar sistema (Login)
Admin --> Frontend : Gerenciar sistema

Frontend --> Backend : Enviar/Receber requisições
Backend --> [Banco de Dados] : Operações CRUD
@enduml""",


}


results = {}
for name, text in diagrams.items():
    results[name] = save_diagram_hex(text, f"{name}_hex.png")


print(results)
