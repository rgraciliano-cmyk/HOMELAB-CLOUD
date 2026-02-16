🛡️ Automação de Backup Híbrido: Local para Cloud (Python)
Este projeto consiste em um script de automação desenvolvido para garantir a integridade e a retenção de dados críticos, realizando o backup de um servidor em 
instância na nuvem (Oracle Cloud Infrastructure) para um servidor local (Bare Metal Dell PowerEdge)

📌 Funcionalidades
Compactação On-the-fly: Utiliza compressão Gzip (tar.gz) para otimizar o tráfego de rede e o espaço em disco.
Transporte Seguro: Transferência de dados via túnel criptografado SSH/SFTP (Porta 22) utilizando a biblioteca Paramiko.
Gestão de Retenção (30 dias): Lógica inteligente que acumula 30 backups diários e, ao atingir o limite, os consolida em um único pacote mensal, reiniciando o ciclo.
Monitoramento e Logs: Sistema de logging detalhado para auditoria de processos e diagnóstico de falhas.
Notificações SMTP: Envio automático de relatórios de status (Sucesso/Falha) via e-mail.

🖥️ Arquitetura do Projeto
🛠️ Tecnologias Utilizadas
Linguagem: Python 3.x
Ambiente Local: Proxmox VE rodando em Hardware Dell
Ambiente Cloud: Oracle Cloud (Ubuntu Instance)
Protocolos: SSH, SFTP, SMTP

🚀 Como Executar
Pré-requisitos:
Possuir chaves SSH configuradas entre o servidor local e a nuvem.
Configurar uma "Senha de Aplicativo" no Gmail para o envio de e-mails.
Instalação de Dependências:

Bash
pip install paramiko
Agendamento (Cron):
Para executar o backup diariamente às 03:00 AM:

Bash
00 03 * * * /usr/bin/python3 /caminho/do/script.py
📚 Lições Aprendidas (Visão de Analista)
Como Analista de Infraestrutura Júnior, a implementação deste projeto reforçou a importância da automação para evitar falhas humanas em processos críticos. 
A integração de scripts Python com o agendamento nativo do Linux (Crontab) permite uma gestão de infraestrutura muito mais eficiente e segura.
