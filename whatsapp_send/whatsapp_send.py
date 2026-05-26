import pywhatkit as kit
import pandas as pd
import time

def whatsapp_send():
    # 1. Configurações (Substitua pelo número de destino com o DDI +55 e DDD)
    # Exemplo: "+5519999999999"
    NUMERO_DESTINO = "+5519981751514" 
    LIMITE_MINIMO = 30
    
    # 2. Ler o CSV e filtrar
    df = pd.read_csv('csv/produtos.csv', sep=';', decimal=',')
    
    # Filtra produtos com estoque baixo
    itens_baixos = df[df['Qtde_Disponivel'] < LIMITE_MINIMO]
    
    if itens_baixos.empty:
        print("Estoque seguro. Nenhuma mensagem de WhatsApp necessária.")
        return

    print(f"Encontrado(s) {len(itens_baixos)} item(ns) para o WhatsApp. Preparando texto...")

    # 3. Montar a mensagem de texto formatada para WhatsApp (usando * para negrito)
    mensagem = "⚠️ *ALERTA DE ESTOQUE BAIXO* ⚠️\n\n"
    mensagem += "Os seguintes produtos precisam de reposição urgente:\n\n"
    
    for _, row in itens_baixos.iterrows():
        mensagem += f"• *{row['Produto']}* - Apenas {int(row['Qtde_Disponivel'])} un.\n"
        
    mensagem += "\n_Mensagem enviada automaticamente pelo Sistema de Monitoramento._"

    try:
        print("Abrindo o WhatsApp Web para enviar... Não mexa no mouse ou teclado.")
        
        # Envia a mensagem instantaneamente. 
        # O parâmetro 'wait_time=15' aguarda 15 segundos para o WhatsApp Web carregar antes de enviar.
        # 'tab_close=True' fecha a aba do navegador automaticamente após o disparo.
        kit.sendwhatmsg_instantly(
            phone_no=NUMERO_DESTINO, 
            message=mensagem, 
            wait_time=15, 
            tab_close=True
        )
        
        # Uma pequena pausa para garantir que o navegador processe o envio antes do script fechar
        time.sleep(3)
        print("Mensagem de WhatsApp enviada com sucesso!")
        
    except Exception as e:
        print(f"Erro ao enviar mensagem no WhatsApp: {e}")