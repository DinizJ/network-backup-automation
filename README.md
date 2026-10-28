# 🌐 Network Configuration Backup Automation

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Netmiko](https://img.shields.io/badge/library-Netmiko-orange)

Projeto automatizado em Python para rotinas de backup da configuração ativa (`running-config`) de switches e roteadores de rede corporativos via SSH, utilizando **Netmiko** e **PyTest**.

---

## 📌 Visão Geral

Este projeto resolve o desafio de gerenciamento contínuo de atualizações e compliance de infraestrutura. Ele se conecta de forma sequencial ou automatizada a ativos de rede (Cisco IOS, HPE/Aruba, etc.), coleta a configuração corrente e gera arquivos rotulados com timestamp na pasta de backups.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Netmiko** (Abstração de conexões SSH/Telnet em ecossistemas multi-vendor)
- **PyYAML** (Manipulação de inventário estruturado)
- **PyTest** (Testes unitários e rotinas de mock sem necessidade de hardware físico)

---

## 📂 Estrutura do Repositório

```text
network-backup-automation/
├── backups/             # Diretório onde os arquivos de backup (.cfg) são armazenados
│   └── .gitkeep
├── inventory/
│   └── hosts.yaml       # Arquivo de inventário com os ativos de rede
├── tests/
│   └── test_backup.py   # Testes unitários com Mocks
├── backup_network.py    # Script principal de execução da automação
├── requirements.txt     # Dependências do projeto Python
├── .gitignore           # Ignora arquivos de backup reais e dados sensíveis
└── README.md            # Documentação completa do repositório
```

---

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/network-backup-automation.git
cd network-backup-automation
```

### 2. Criar e Ativar o Ambiente Virtual (Recomendado)
```bash
python -m venv venv
# No Linux/macOS:
source venv/bin/activate
# No Windows:
.env\Scriptsctivate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar o Inventário de Ativos
Edite o arquivo `inventory/hosts.yaml` com as informações do seu ambiente:
```yaml
- hostname: SW-ACCESS-01
  ip: 192.168.1.10
  device_type: cisco_ios
  username: admin
  password: SecretPassword123!
```

### 5. Executar a Automação
```bash
python backup_network.py
```

---

## 🧪 Executando os Testes Unitários

Para garantir que o código funcione corretamente sem precisar conectar a dispositivos reais de rede, execute a suíte de testes com **PyTest**:

```bash
pytest -v
```

---

## 🛡️ Segurança

- As senhas não devem ser expostas diretamente no código-fonte.
- O repositório já inclui um arquivo `.gitignore` configurado para não subir históricos de configurações geradas ou variáveis de ambiente locais.
