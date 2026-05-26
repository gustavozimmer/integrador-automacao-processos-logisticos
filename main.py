from html_create.html_create import start_site
from excel_create.excel_create import export_to_excel
from email_send.email_send import email_send
from whatsapp_send.whatsapp_send import whatsapp_send

email_send()
export_to_excel()
whatsapp_send()
start_site()