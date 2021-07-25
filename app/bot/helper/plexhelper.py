from plexapi.myplex import MyPlexAccount
import re
from app.bot.helper.confighelper import Plex_LIBS
import logging
logging.basicConfig(filename="app/config/plex.log", filemode='a', level=logging.ERROR)

def plexadd(plex, plexname):
    global Plex_LIBS
    try:
        if Plex_LIBS[0] == "all":
            Plex_LIBS = plex.library.sections()
        plex.myPlexAccount().inviteFriend(user=plexname, server=plex, sections=Plex_LIBS, allowSync=False,
                                              allowCameraUpload=False, allowChannels=False, filterMovies=None,
                                              filterTelevision=None, filterMusic=None)
        logging.info(plexname +' has been added to plex')
        return True
    except Exception as e:
        logging.error(e)
        return False

def plexremove(plex, plexname):
    try:
        plex.myPlexAccount().removeFriend(user=plexname)
        logging.info(plexname +' has been removed from plex')
        return True
    except Exception as e:
        logging.error(e)
        return False
        '''

        plex python api has no tools to remove unaccepted invites... 

        logging.info("Trying to remove invite...")
        removeinvite = plexremoveinvite(plex, plexname)
        if removeinvite:
            return True
        '''
        
'''
def plexremoveinvite(plex, plexname):
    try:
        plex.myPlexAccount().removeFriend(user=plexname)
        logging.info(plexname +' has been removed from plex')
        return True
    except Exception as e:
        logging.error(e)
        return False        
'''
def verifyemail(addressToVerify):
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
    match = re.match(regex, addressToVerify)
    if match == None:
	    return False
    else:
        return True