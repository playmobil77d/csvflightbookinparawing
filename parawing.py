# -*- coding: utf-8 -*-

import cookielib
import re
import sys
import urllib
import urllib2

from urllib2 import Request


import mimetypes, mimetools

carnet_parawing_root = "http://carnet.parawing.net/"
# Config Proxy
host="web-lyon1.sncf.fr"
port="8080"
proxy_user = 'COMMUN\pdbs10841'
proxy_password_orig='sncf0411'

def post_multipart(url, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        print "%s: %s" %(key, value)
        L.append(value.decode('utf-8').encode('utf-8'))
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        #L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value.decode('utf-8').encode('utf-8'))
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

class ParawingException(Exception):
    def __init__(self, message):
        """On se contente de stocker le message d'erreur"""
        self.message = message

    def __str__(self):
        """On retourne le message"""
        return self.message


class Carnet:
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.cookie = None
        self.ua = {'User-agent':'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1.1) Gecko/20090715 Firefox/3.6'}
        
    def connect(self, username, password):
        
        #Proxy
        '''proxy_password = urllib2.quote(proxy_password_orig, "")
        proxy_url = 'http://' + proxy_user + ':' + proxy_password + '@' + host+ ':' + port
        proxy_support = urllib2.ProxyHandler({"http":proxy_url})
        opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)'''
        
        
        url_connect = carnet_parawing_root + "login.php"
        data = urllib.urlencode({'login'    : username,'pass' : password})
        r = self.opener.open(url_connect)
        #txheaders = {'User-agent' : self.ua}

        try:
            req = Request(url_connect, data)
            handle = self.opener.open(req)

            for i in handle.readlines():
                m = re.search("Login ou mot de passe incorrect.", i)
                if m != None:
                    raise ParawingException("Login failed")
                        
            for index, cookie in enumerate(self.cj):
                self.cookie = "%s=%s" %(cookie.name, cookie.value)
                break # only one...!

            if self.cookie == None:
                print("No cookie found, login failed")
        
        except ParawingException:
            print "Login Failed ! Try again !"
            sys.exit(0)
                        
        except IOError, e:
            print 'Error opening "%s".' % url_connect
            if hasattr(e, 'code'):
                print 'Error code - %s.' % e.code
            elif hasattr(e, 'reason'):
                print "Reason :", e.reason
                print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
                raise ParawingException("Error login with username [%s]" %username)

    def newFlight(self, vol):
        if self.cookie == None:
            raise ParawingException("Login first")
        
        url = carnet_parawing_root + "insert_vol.php"
        
        form = {}

######### Champ obligatoire :
        
        # Date
        form['jour'] = str(vol.ddate.tm_mday)
        form['mois'] = str(vol.ddate.tm_mon)
        form['annee'] = str(vol.ddate.tm_year)

        # Décollage
        form['flag_site'] = '0'
        form['site_db_check'] = 'on'
        form['site_db'] = vol.deco

        # Atterrissage
        form['flag_site_atterro'] = '0'
        form['atterro_db_check'] = 'on'
        form['atterro_db'] = vol.atterro

        # Aile
        form['aile'] = vol.aile
        form['flag_aile'] = '1'
        # if newaile enabled, then a new wing is added
        #form['newaile'] = ""

        # Durée
        form['duree'] = str(vol.duration)
        
######### Champ Facultatif :

        dicotype = {'Gonflage' : '1',
                     'Pente ecole' : '10',
                     'Bi pédagogique' : '15',
                     'Plouf' : '20',
                     'Grand vol' : '30',
                     'Vol local' : '40',
                     'Cross' : '50',
                     'Triangle FAI' : '51',
                     'Triangle' : '52',
                     'Vol rando' : '60',
                     'Vol à ski' : '61',
                     'Speed riding' : '62',
                     'Vol treuil' : '70',
                     'Paramoteur' : '71',
                     'Pilotage' : '79',
                     'SIV' : '80',
                     'Seance wagas' : '90',
                     'Seance voltige' : '95',
                     'Competition A' : '96',
                     'Competition B' : '97',
                     'Planeur' : '101',
                     'Delta' : '102',
                     'Autre' : '255'}

        form['type'] = dicotype[vol.vtype]
         
        # if enabled, this is a bi
        #form['biplace']
        
        # Takeoff time (free)
        form['heure'] = vol.hdeco

        form['cond_deco'] = str(vol.conddeco)
        form['cond_vol'] = str(vol.condvol)
        form['cond_aterro'] = str(vol.condatterro)

        # in km, max 999
        form['distance'] = str(vol.dist)

        # in m, max 9999
        form['alt_max'] = str(vol.altmax)
        form['pt_bas'] = str(vol.lowestpt)

        # in m, max 9999
        form['gain_max'] = str(vol.maxgain)
        
        # in m, max 99999
        form['gain_total'] = str(vol.gaintotal)

        # free text
        form['contournement'] = ""

        # if enabled, instrument are used
        #form['instrument']

        dicocadre = {'Ecole':'1',
                  'Club':'2',
                  'Entre potes':'3',
                  'Autonome':'4'}

        form['cadre'] = dicocadre[vol.encadrement]        
        form['stage_check'] = 'no'

        # free text, max 50chars
        form['compagnons'] = str(vol.pote)

        form['recit'] = vol.story

        # http link to pictures, without leading http
        form['photos'] = str(vol.photo)

        # upload GPS trace
        # form['file']

        diconote = {'Nul':'1',
                  'Bof':'2',
                  'Pas mal':'3',
                  'Top':'4',
                  'Genial !':'5'}

        form['ma_note'] = diconote[vol.note]

        # if enabled, will be published
        #form['visible'] = 

        form['choix'] = "Ajouter"
    
        
        content_type, body = encode_multipart_formdata(form.items(), {})
        headers = {'Content-Type': content_type,
                   'Content-Length': str(len(body))}
        
        try:
            req = urllib2.Request(url, body, headers)
            print form
            handle = self.opener.open(req)
        except IOError:
            print 'Cela a foiré !'
        else:
            print req

        # handle.read() renvoie la page
        # handle.geturl() renvoie la véritable url de la page demandée
        # (au cas où urlopen a été redirigé, ce qui arrive parfois)
         
    def listAile(self, username):
        if self.cookie == None:
            print("Login first")
        
        liste_aile = list()
        liste_aile = ['Mescal','Rush2','ZuluXP']
        
        '''proxy_password = urllib2.quote(proxy_password_orig, "")
        proxy_url = 'http://' + proxy_user + ':' + proxy_password + '@' + host+ ':' + port
        proxy_support = urllib2.ProxyHandler({"http":proxy_url})
        opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)'''
        
        #recup aile pilote
        #url_aile = carnet_parawing_root + "serv_get_aile?pilote=" + username + "&key=cavole"   
        
        
        
        #f = urllib2.urlopen('http://www.python.org/')
        
        #http://carnet.parawing.net/serv_get_aile?pilote=pirk&key=cavole
      
        #page_aile = urllib.urlopen(url_aile)
        #str_page_aile=page_aile.read()
        
        #for aile in str_page_aile.split("\n"):
        #    if aile != "":
        #        liste_aile.append(aile)
        
        return liste_aile
      
      
      
   
    def listDeco(self):
        # recup liste deco
        return "NA"
   
    def listAtterro(self):
        #recup liste atterro
        return "NA"
