import os
import datetime
import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def load_inventory(inventory_file="inventory/hosts.yaml"):
    """Carrega o arquivo de inventário YAML com as credenciais e IPs dos ativos."""
    if not os.path.exists(inventory_file):
        raise FileNotFoundError(f"Arquivo de inventário '{inventory_file}' não encontrado.")
    with open(inventory_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def backup_device(device, output_dir="backups"):
    """Executa o backup das configurações salvas (running-config) via SSH."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    hostname = device.get("hostname", device.get("ip"))
    filename = f"{output_dir}/{hostname}_{timestamp}.cfg"

    device_params = {
        "device_type": device.get("device_type", "cisco_ios"),
        "host": device.get("ip"),
        "username": device.get("username"),
        "password": device.get("password"),
        "timeout": 10,
    }

    try:
        print(f"[+] Conectando ao ativo {hostname} ({device['ip']})...")
        connection = ConnectHandler(**device_params)
        connection.enable()
        
        # Coleta a configuração ativa
        output = connection.send_command("show running-config")
        connection.disconnect()

        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"[✓] Backup concluído com sucesso: {filename}")
        return True, filename

    except NetmikoTimeoutException:
        print(f"[✗] Erro: Timeout na conexão com {hostname} ({device['ip']}).")
        return False, "Timeout"
    except NetmikoAuthenticationException:
        print(f"[✗] Erro: Falha de autenticação no ativo {hostname} ({device['ip']}).")
        return False, "Auth Failure"
    except Exception as e:
        print(f"[✗] Erro inesperado ao processar {hostname}: {str(e)}")
        return False, str(e)

def run_backup_job():
    """Função principal que percorre todo o inventário de rede."""
    devices = load_inventory()
    print(f"=== Iniciando Job de Backup ({len(devices)} ativos localizados) ===")
    results = {}
    for dev in devices:
        status, detail = backup_device(dev)
        results[dev.get("hostname")] = status
    return results

if __name__ == "__main__":
    run_backup_job()
