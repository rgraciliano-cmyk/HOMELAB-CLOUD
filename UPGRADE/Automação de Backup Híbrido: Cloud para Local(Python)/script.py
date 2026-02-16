import os
import tarfile
import paramiko
import smtplib
import logging
from email.message import EmailMessage
from datetime import datetime

# --- CONFIGURAÇÕES DE CAMINHO ---
PASTA_LOCAL = '/caminho/da/sua/pasta'
PASTA_REMOTA = '/home/ubuntu/backups'
LOG_FILE = '/var/log/backup_diario.log'

# --- CONFIGURAÇÕES DE E-MAIL (Use App Passwords se for Gmail) ---
EMAIL_REMETENTE = "seu-email@gmail.com"
EMAIL_DESTINATARIO = "seu-email@gmail.com"
SENHA_EMAIL = "sua-senha-app" # Nunca use a senha real, use senha de aplicativo

# --- CONFIGURAÇÕES SSH/NUVEM ---
HOST_NUVEM = 'seu_ip_oracle'
USUARIO = 'ubuntu'
CHAVE_SSH = '/home/usuario/.ssh/id_rsa'

# Configuração de Logs
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def enviar_email(status, detalhes):
    msg = EmailMessage()
    msg.set_content(f"Relatório de Backup\nStatus: {status}\n\nDetalhes:\n{detalhes}")
    msg['Subject'] = f"Status Backup: {status} - {datetime.now().strftime('%d/%m/%Y')}"
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_EMAIL)
            smtp.send_message(msg)
    except Exception as e:
        logging.error(f"Falha ao enviar e-mail: {e}")

def executar_backup():
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"backup_{data_hoje}.tar.gz"
    
    try:
        logging.info("Iniciando compactação...")
        with tarfile.open(nome_arquivo, "w:gz") as tar:
            tar.add(PASTA_LOCAL, arcname=os.path.basename(PASTA_LOCAL))
        
        logging.info(f"Conectando ao servidor {HOST_NUVEM}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST_NUVEM, port=22, username=USUARIO, key_filename=CHAVE_SSH)
        
        sftp = ssh.open_sftp()
        sftp.put(nome_arquivo, os.path.join(PASTA_REMOTA, nome_arquivo))
        logging.info("Upload concluído com sucesso.")

        # Lógica de rotação (30 dias)
        arquivos = [f for f in sftp.listdir(PASTA_REMOTA) if f.endswith('.tar.gz')]
        if len(arquivos) >= 30:
            mes = datetime.now().strftime("%B_%Y")
            comando = f"cd {PASTA_REMOTA} && tar -czf consolidado_{mes}.tar.gz *.tar.gz --remove-files"
            ssh.exec_command(comando)
            logging.info(f"Rotação mensal executada: consolidado_{mes}.tar.gz")

        sftp.close()
        ssh.close()
        os.remove(nome_arquivo)
        
        detalhes = f"Backup {nome_arquivo} realizado e enviado para a nuvem.\nLogs: {LOG_FILE}"
        enviar_email("SUCESSO", detalhes)
        logging.info("Processo finalizado com sucesso.")

    except Exception as e:
        erro_msg = f"Erro durante o backup: {str(e)}"
        logging.error(erro_msg)
        enviar_email("FALHA", erro_msg)

if __name__ == "__main__":
    executar_backup()
