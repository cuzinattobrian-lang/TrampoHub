# TrampoHub

## Nexus Talentos S.A.

O **TrampoHub** é uma plataforma web desenvolvida em Python com Flask para conectar profissionais em busca de oportunidades de trabalho a empresas que procuram novos talentos. O sistema permite o gerenciamento dinâmico de candidaturas, validações de back-end, métricas em tempo real e controle de status.

---

## 👥 Integrantes

- Pedro Henrique Lima de Amorim — RM: [19255]
- Brian Iha Cuzinatto — RM: [22550]
- Jean Alcaras — RM: [17129]
- Luan Gonçalves Mesquita  — RM: [22866]
- Miguel Pinheiro Farias Nunes — RM: [22559]

---

## 🚀 Funcionalidades Principais

- **Validação de Back-end:** O servidor rejeita envios com campos vazios ou dados inválidos.
- **Dashboard de Métricas:** Cards dinâmicos na página inicial com contadores em tempo real.
- **Controle de Estado:** Botão para alternar o status da candidatura diretamente na tabela (ex: *Em Análise* / *Aprovado*).
- **Filtro e Busca:** Pesquisa rápida de registros por nome ou vaga na tabela.

---

## 🛠️ Tecnologias Utilizadas

- **Python & Flask** (Back-end e rotas)
- **HTML5 & CSS3** (Front-end e estilização)
- **Git & GitHub** (Controle de versão)

---

## 📊 Estrutura de Dados (DER Lógico)

Como o projeto armazena os dados em memória (dicionários e listas do Python), a estrutura lógica da entidade **Candidatura** é representada abaixo:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | Inteiro | Identificador único gerado automaticamente |
| `nome` | String | Nome completo do candidato |
| `email` | String | E-mail de contato do candidato |
| `vaga` | String | Título da vaga pretendida |
| `modalidade` | String | Presencial, Híbrido ou Remoto |
| `contrato` | String | CLT, PJ ou Estágio |
| `status` | String | Estado atual da candidatura (*Em Análise* / *Aprovado*) |

---

## 🗺️ Tabela de Rotas Mapeadas

| Rota | Método HTTP | Descrição |
| :--- | :--- | :--- |
| `/` | `GET` | Página inicial contendo os cards de métricas, barra de busca e tabela de candidaturas. |
| `/formulario` | `GET` | Exibe a página com o formulário de cadastro de nova candidatura. |
| `/cadastrar` | `POST` | Processa os dados enviados, aplica as validações de back-end e salva na memória. |
| `/mudar-status/<int:id>` | `POST` | Altera o estado/status de uma candidatura específica na memória. |

---

## 📁 Estrutura do Projeto

```text
TrampoHub/
├── app.py
├── .gitignore
├── README.md
├── docs/
│   └── der.png
├── static/
│   └── style.css
└── templates/
    ├── index.html
    └── formulario.html