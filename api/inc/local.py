# -*- coding: utf-8 -*-
# localisation
import re

languages = [ 'en', 'es', 'ru', 'zh' ]

es = {'{{Owner}}'         : 'Propietario', 
      '{{Issuer}}'        : 'Emisor', 
      '{{Decimals}}'      : 'Decimales', 
      '{{Asset ID}}'      : 'ID del activo', 
      '{{Init amount}}'   : 'Cantidad inicial', 
      '{{ASK}}'           : 'Demanda', 
      '{{BID}}'           : 'Oferta', 
      '{{Volume}}'        : 'Volumen',
      '{{Ask Orders}}'    : 'Órdenes de Venta',
      '{{Bid Orders}}'    : 'Órdenes de Compra',
      '{{Price}}'         : 'Precio',
      '{{Quantity}}'      : 'Cantidad',
      '{{Total}}'         : 'Total',
      '{{Send NXT}}'      : 'Enviar NXT',
      '{{Broadcast}}'     : 'Transmitir',
      '{{News}}'          : 'Noticias',
      '{{Settings}}'      : 'Ajustes',
      '{{Address}}'       : 'Dirección',
      '{{Save}}'          : 'Guardar',
      '{{Menu}}'          : 'Menú',
      '{{Recipient}}'     : 'Destinatario',
      '{{Nxt address}}'   : 'Dirección Nxt',
      '{{Message}}'       : 'Mensaje',
      '{{Your short message}}' : 'Tu pequeño mensaje',
      '{{amount}}'        : 'cantidad',
      '{{Send}}'          : 'Enviar',
      '{{Close}}'         : 'Cerrar',
      '{{Your account does not have public key!}}' : 'Tu cuenta no dispone de clave pública!',

      }

ru = {'{{Owner}}'         : 'Владелец', 
      '{{Issuer}}'        : 'Владелец', 
      '{{Decimals}}'      : 'Разрядов', 
      '{{Asset ID}}'      : 'Номер ассета', 
      '{{Init amount}}'   : 'Начальное кол-во', 
      '{{ASK}}'           : 'Покупка', 
      '{{BID}}'           : 'Продажа', 
      '{{Volume}}'        : 'Объем',
      '{{Ask Orders}}'    : 'Ордеры на покупку',
      '{{Bid Orders}}'    : 'Ордеры на продажу',
      '{{Price}}'         : 'Цена',
      '{{Quantity}}'      : 'Количество',
      '{{Total}}'         : 'Всего', 
      '{{Send NXT}}'      : 'Отправить NXT',
      '{{Broadcast}}'     : 'Транслировать',
      '{{News}}'          : 'Новости',
      '{{Settings}}'      : 'Настройки',
      '{{Address}}'       : 'Адрес',
      '{{Save}}'          : 'Сохранить',
      '{{Menu}}'          : 'Меню',
      '{{Recipient}}'     : 'Адрес',
      '{{Nxt address}}'   : 'Nxt',
      '{{Message}}'       : 'Сообщение',
      '{{Your short message}}' : 'Ваше короткое сообщение',
      '{{amount}}'        : 'количество',
      '{{Send}}'          : 'Отправить',
      '{{Close}}'         : 'Закрыть',
      '{{Your account does not have public key!}}' : 'Ваша адрес не имеет публичного ключа!',

      }

zh = {'{{Owner}}'        : '所有者',
      '{{Issuer}}'        : '发行者',
      '{{Decimals}}'      : '小数位',
      '{{Asset ID}}'      : '资产 ID',
      '{{Init amount}}'   : '初始总量',
      '{{ASK}}'           : '卖',
      '{{BID}}'           : '买',
      '{{Volume}}'        : '交易量',
      '{{Ask Orders}}'    : '卖单',
      '{{Bid Orders}}'    : '买单',
      '{{Price}}'         : '价格',
      '{{Quantity}}'      : '数量',
      '{{Total}}'         : '总量',
      '{{Send NXT}}'      : '发送NXT',
      '{{Broadcast}}'     : '广播',
      '{{News}}'          : '新闻',
      '{{Settings}}'      : '设置',
      '{{Address}}'       : '地址',
      '{{Save}}'          : '保存',
      '{{Menu}}'          : '菜单',
      '{{Recipient}}'     : '收件人',
      '{{Nxt address}}'   : 'NXT地址',
      '{{Message}}'       : '信息',
      '{{Your short message}}' : '你的短信',
      '{{amount}}'        : '总额',
      '{{Send}}'          : '发送',
      '{{Close}}'         : '关闭',
      '{{Your account does not have public key!}}' : '你的账户没有公钥',

     }



dd = {'{{Owner}}'         : '', 
      '{{Issuer}}'        : '', 
      '{{Decimals}}'      : '', 
      '{{Asset ID}}'      : '', 
      '{{Init amount}}'   : '', 
      '{{ASK}}'           : '', 
      '{{BID}}'           : '', 
      '{{Volume}}'        : '',
      '{{Ask Orders}}'    : '',
      '{{Bid Orders}}'    : '',
      '{{Price}}'         : '',
      '{{Quantity}}'      : '',
      '{{Total}}'         : '',
      '{{Send NXT}}'      : '',
      '{{Broadcast}}'     : '',
      '{{News}}'          : '',
      '{{Settings}}'      : '',
      '{{Address}}'       : '',
      '{{Save}}'          : '',
      '{{Menu}}'          : '',
      '{{Recipient}}'     : '',
      '{{Nxt address}}'   : '',
      '{{Message}}'       : '',
      '{{Your short message}}' : '',
      '{{amount}}'        : '',
      '{{Send}}'          : '',
      '{{Close}}'         : '',
      '{{Your account does not have public key!}}' : '',
      '{{You have not any Assets}}' : '',
      }



def translate(text, lang='en'):
  """ replace all {{...}} -> translated variant"""
  if lang not in languages:
    lang = 'en'

  regex = re.compile( '{{.*}}' )

  # result
  res = text
  matches = set()

  for match in regex.finditer(text):
    matches.add( match.group() )

  for item in matches:
    #print ("""Replace %s to %s""" % (item, _(item, lang) ) )
    res = res.replace( item, _(item, lang) )

  return res


# translate {{WORD}} -> to other lang
def _(s, lang='en'):

  if ( lang == 'en' ):
    return s.replace('{{','').replace('}}','')

  if ( lang == 'es' ):
    if s in es:
      return es[s]
    else:
      return s.replace('{{','').replace('}}','')

  if ( lang == 'ru' ):
    if s in ru:
      return ru[s]
    else:
      return s.replace('{{','').replace('}}','')

  if ( lang == 'zh' ):
    if s in zh:
      return zh[s]
    else:
      return s.replace('{{','').replace('}}','')

  
 
