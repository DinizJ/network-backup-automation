import pytest
import os
from unittest.mock import patch, MagicMock
from backup_network import load_inventory, backup_device

def test_load_inventory(tmp_path):
    # Teste de carregamento do inventário YAML
    test_yaml = tmp_path / "hosts.yaml"
    test_yaml.write_text("""
- hostname: TEST-SW
  ip: 10.0.0.1
  device_type: cisco_ios
""")
    inventory = load_inventory(str(test_yaml))
    assert len(inventory) == 1
    assert inventory[0]["hostname"] == "TEST-SW"

@patch("backup_network.ConnectHandler")
def test_backup_device_success(mock_connect_handler, tmp_path):
    # Teste simulado (mock) de execução de backup via SSH
    mock_connection = MagicMock()
    mock_connection.send_command.return_value = "building configuration... running-config mock output"
    mock_connect_handler.return_value = mock_connection

    device = {
        "hostname": "SW-MOCK-01",
        "ip": "10.0.0.10",
        "device_type": "cisco_ios",
        "username": "admin",
        "password": "password"
    }

    output_dir = str(tmp_path / "backups")
    status, filepath = backup_device(device, output_dir=output_dir)

    assert status is True
    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        content = f.read()
    assert "running-config mock output" in content
