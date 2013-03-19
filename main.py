# -*- coding: utf-8 -*-

"""
Explain what program do.
"""

from parawing import Carnet
from vol import Vol
import csv
import getpass
import os
import sys
from optparse import OptionParser

def main():
    """ Main function, deals with arguments and launch program"""
    # Usual verifications and warnings
    if not sys.argv[1:]:
        sys.stdout.write("Sorry: you must specify at least an argument\n")
        sys.stdout.write("More help avalaible with -h or --help option\n")
        sys.exit(0)

    usage = "usage: %prog [options] arg1 arg2 ..."
    parser = OptionParser(usage=usage)
    
    parser.add_option("-i", "--input_file", dest="input_filename",
                      help="Read input from <file>.", metavar="<file>")
   
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    parser.add_option("-v", "--verbose", 
                      action="store_true", dest="verbose", default=False,
                      help="Write output informations (not only errors).")

    (options, args) = parser.parse_args()

    return options.input_filename


if __name__ == '__main__':
    argument = main()   
    parawing = Carnet()
    liste_vol = list()
    liste_aile = list()
    print argument
    # Connexion au site
    #login = raw_input("Login : ")
    #mdp = getpass.getpass("Mot de passe : ")
    username = "playmotest"
    mdp = "playmote"
    parawing.connect(username,mdp)
    
    #Recuperation des ailes du pilote enregistre sur Parawing
    liste_aile = parawing.listAile(username)
    
    #Ouverture du fichier csv passe en argument
    fic = open(argument,"rb")

    try:
        reader = csv.DictReader(fic)
        
        for row in reader:
            print row
            v = Vol(row['day'],row['deco'],row['atterro'],"ZuluXP",row['duree'],row['typev'],row['hdeco'],row['conddeco'],"",row['condatterro'],row['km'],row['altmax'],row['variomax'],row['altgain'],row['variomin'],True,"Autonome","",row['story'],"","Pas mal")
         
            # Test aile
            print v.compareAile(liste_aile)
         
            # Test deco
            # ex : parawing.testdeco
         
            # Test atterro
            # ex : parawing.testatterro
         
            #ajout du vol a un objet list
            #liste_vol.append(v)
   
    except csv.Error, e:
        sys.exit('file %s, line %d: %s' % (argument, reader.line_num, e))
       
    finally:
        fic.close()
   
    #Affichage du nombre de vol dans la liste
    #print len(liste_vol)
      
    #Demande de confirmation d'upload des vols
    #confirmation = raw_input("Confirmer vous l'import des vols sur Parawing ? (Oui/Non) ")
    
    #Initialisation compteur boucle
    '''i = 0  
    if confirmation == "Oui":
        while i<len(liste_vol):
            # Add Fly to Parawing's flybook
            #parawing.newFlight(liste_vol[i])
            print(liste_vol[i])
            i += 1
    else:
        print("Importation annulée")'''
