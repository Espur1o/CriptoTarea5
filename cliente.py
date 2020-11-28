import imaplib, email 
import re

user = ''
password = ''
imap_url = 'imap.gmail.com'



sender = 'info@i.drop.com'
expreg= "^[0-9A-F]{2}.[0-9A-F]{2}.[0-9]{5}.[0-9A-F]{6}F5@[a-z]{2}.mta2vrest.cc.prd.sparkpost$"
verify = 'messageid.txt'

# Obtenemos el cuerpo del correo
def get_body(msg): 
    if msg.is_multipart(): 
        return get_body(msg.get_payload(0)) 
    else: 
        return msg.get_payload(None, True) 

# Hacemos busqueda en base a parametros
def search(key, value, con): 
    result, data = con.search(None, key, '"{}"'.format(value)) 
    return data 

# Se obtiene el messageID de los correos
def get_emails(result_bytes): 
    msgs = []
    for num in result_bytes[0].split(): 
        typ, data = con.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])') #se obtiene el messageid desde el header
        msgs.append(data) 

    return msgs 

def checkMID(pattern,message):
    if bool(re.match(pattern, message)) == False:
        print ('el messageID: '+message+' no corresponde a la expresión regular.'   )
    else:
        print('El correo es válido.')




checkCorreo = input('Desea ingresar un correo emisor?(Y/N): ')
if checkCorreo=='Y':
    sender = input('Ingrese el correo emisor: ')
    expreg= input('Ingrese la expresion regular correspondiente: ')
    verify = input('Ingrese el archivo txt con los messageID')
    arch = open(verify)
    
else:
    print('Se revisarán los correos por defecto')

pattern = re.compile(expreg)

# conexion ssl
con = imaplib.IMAP4_SSL(imap_url) 

# logeamos con la cuenta usada
con.login(user, password) 

# obtenemos la bandeja de entrada del correo logeado
con.select('Inbox') 

# se eligen los correos en base a su emisor
msgs = get_emails(search('FROM', sender , con)) 

archive = open(verify,'w')
for msg in msgs: #msgs[::-1]
    for sent in msg: 
        if type(sent) is tuple: 
            content = str(sent[1], 'utf-8')    
            indexstart = content.find("<")#dentro del message id
            indexend = content.find(">")
            mid = content[indexstart+1:indexend]
            archive.write(str(mid) + '\n')
archive.close()

arch = open(verify)
for i in arch:
    i = i.strip()
    checkMID(pattern,i)
arch.close()

dyw = input('Desea ingresar un message ID para comparar con el emisor'+str(sender) + '?(Y/N)')
while dyw == 'Y':    
    check = input("Ingrese un messageID:")
    if check=='':
        break
    checkMID(pattern,check)






           

