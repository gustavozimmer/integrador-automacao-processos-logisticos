import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

def email_send():
    # 1. Configurações do e-mail (Substitua pelos seus dados)
    EMAIL_REMETENTE = "testedeemailteste67@gmail.com"
    SENHA_APP = "xjhu igsq lwvw iegm"  # Não é a senha normal, veja a nota abaixo!
    EMAIL_DESTINATARIO = "zimaonofoco@gmail.com"
    
    LIMITE_MINIMO = 30  # Define o que é "estoque acabando"
    
    # 2. Ler o CSV e filtrar os itens
    df = pd.read_csv('csv/produtos.csv', sep=';', decimal=',')
    
    # Filtra os produtos com estoque baixo
    # (Ajuste o nome das colunas 'ESTOQUE' e 'PRODUTO' conforme o seu arquivo)
    itens_baixos = df[df['Qtde_Disponivel'] < LIMITE_MINIMO]
    
    # Se não houver nenhum item acabando, interrompe a função
    if itens_baixos.empty:
        print("Todos os produtos estão com estoque seguro. Nenhum e-mail enviado.")
        return

    print(f"Encontrado(s) {len(itens_baixos)} item(ns) com estoque baixo. Preparando e-mail...")

    # 3. Construir a lista de produtos em HTML
    linhas_tabela = ""
    for _, row in itens_baixos.iterrows():
        linhas_tabela += f"""
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'>{row['Produto']}</td>
            <td style='padding: 8px; border: 1px solid #ddd; text-align: center; color: red; font-weight: bold;'>{int(row['Qtde_Disponivel'])}</td>
        </tr>
        """

    corpo_html = f"""
    <html>
        <body style='font-family: Arial, sans-serif;'>
            <h2 style='color: #D9534F;'>⚠️ Alerta: Itens com Estoque Baixo!</h2>
            <p>Os seguintes produtos atingiram o limite crítico (menos de {LIMITE_MINIMO} unidades) e precisam de reposição:</p>
            <table style='border-collapse: collapse; width: 100%; max-width: 500px;'>
                <thead>
                    <tr style='background-color: #f2f2f2;'>
                        <th style='padding: 8px; border: 1px solid #ddd; text-align: left;'>Produto</th>
                        <th style='padding: 8px; border: 1px solid #ddd;'>Qtd Atual</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_tabela}
                </tbody>
            </table>
            <br>
            <p><em>Este é um e-mail automático gerado pelo sistema de monitoramento de estoque.</em></p>
        </body>
    </html>
    """

    # 4. Configurar a mensagem (MIME)
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = "⚠️ ALERTA: Reposição de Estoque Necessária"
    msg.attach(MIMEText(corpo_html, 'html'))

    # 5. Conectar ao servidor SMTP (Exemplo usando o Gmail)
  # 5. Conectar ao servidor SMTP usando SSL (Porta 465)
    try:
        # Mudamos de SMTP para SMTP_SSL e alteramos a porta para 465
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_REMETENTE, SENHA_APP)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        server.quit()
        print("E-mail de alerta enviado com sucesso pela porta 465!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")