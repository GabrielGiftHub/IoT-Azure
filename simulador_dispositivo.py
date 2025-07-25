import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import random
import json
import os  # <<--- Linha NOVA: Importa o módulo 'os' para ler variáveis de ambiente
from dotenv import load_dotenv # <<--- Linha NOVA: Importa o módulo para carregar o .env

load_dotenv() # <<--- Linha NOVA: Carrega as variáveis do arquivo .env

# O script agora lê a string de conexão de uma variável de ambiente.
# Sua cadeia de conexão NÃO DEVE MAIS ESTAR DIRETAMENTE AQUI.
CONNECTION_STRING = os.environ.get("IOTHUB_DEVICE_CONNECTION_STRING")

# <<--- Linhas NOVAS: Verificação para garantir que a chave foi encontrada
if not CONNECTION_STRING:
    print("ERRO: A variável de ambiente 'IOTHUB_DEVICE_CONNECTION_STRING' não foi definida.")
    print("Certifique-se de que sua cadeia de conexão está em um arquivo .env ou definida no ambiente.")
    exit(1) # Sai do script se a string não for encontrada
# <<--- Fim das Linhas NOVAS

async def main():
    # Crie uma instância do cliente do dispositivo IoT Hub
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Conecte o cliente
    await device_client.connect()
    print("Dispositivo conectado ao IoT Hub.")

    # Envie mensagens de telemetria a cada 5 segundos
    for i in range(10): # Enviar 10 mensagens para demonstração
        temperatura = 20 + (random.random() * 10)  # Temperatura entre 20 e 30
        umidade = 60 + (random.random() * 10)     # Umidade entre 60 e 70

        telemetria_data = {
            "temperatura": round(temperatura, 2),
            "umidade": round(umidade, 2),
            "mensagemId": i + 1
        }
        # Converta o dicionário em uma string JSON
        json_message = json.dumps(telemetria_data)

        print(f"Enviando mensagem {i+1}: {json_message}")
        await device_client.send_message(json_message)
        await asyncio.sleep(5)

    # Desconecte o cliente
    await device_client.shutdown()
    print("Dispositivo desconectado.")

if __name__ == "__main__":
    asyncio.run(main())