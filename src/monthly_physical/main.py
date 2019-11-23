# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/MonthlyPhysical
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import os, re, random
from aqt import mw
from aqt.qt import *
from anki.hooks import wrap, addHook

from .config import *


ADDON_NAME='MonthlyPhysical'

config=Config(ADDON_NAME)

IMG_EXT = re.compile(r'\.(?:jpe?g|gif|png|bmp)$', re.I)


def getRandomImage(dir):
    MOD_ABS,_ = os.path.split(__file__)
    dir=os.path.join(MOD_ABS,'images',dir)
    return os.path.join(
        dir,random.choice(
            [i for i in os.listdir(dir) if IMG_EXT.search(i)]
        )
    )


def alert(dir):
    img=getRandomImage(dir)
    mb=QMessageBox(mw)
    mb.setIconPixmap(QPixmap(img))
    mb.setWindowTitle("Reminder:")
    b=mb.addButton(QMessageBox.Ok)
    b.setDefault(True)
    return mb.exec_()


def isLate(type, delayed):
    if delayed:
        today=mw.col.sched.today
        lstMod=mw.col.conf.get(type,-1)
        if lstMod > -1 and today-lstMod>=delayed:
            nag=config.get('days_to_nag_again',3)
            adj=today-delayed+max(1,nag)
            mw.col.conf[type]=adj
            mw.col.setMod()
            return True


def startup_check():
    type=""
    today=mw.col.sched.today

    rDB=config.get('remind_to_check_db_in',28)
    if isLate("chkdb_mod", rDB):
        type+='1'

    rMD=config.get('remind_to_check_media_in',0)
    if isLate("chkmd_mod", rMD):
        type+='2'

    rEC=config.get('remind_to_check_empty_card_in',0)
    if isLate("chkec_mod", rEC):
        type+='3'

    if type:
        alert(type)

addHook('profileLoaded', startup_check)





def log_last_db_checkup(self):
    self.conf["chkdb_mod"]=self.sched.today
    self.setMod()

def log_last_media_checkup(self, *args, **kwargs):
    self.col.conf["chkmd_mod"]=self.col.sched.today
    self.col.setMod()

def log_last_empty_card_checkup(self, *args, **kwargs):
    self.conf["chkec_mod"]=self.sched.today
    self.setMod()


try:
    import ccbc
    ccbc.collection._ExtCollection.fixIntegrity=wrap(
        ccbc.collection._ExtCollection.fixIntegrity,
        log_last_db_checkup, "before"
    )
    ccbc.media.ExtMediaManager.check=wrap(
        ccbc.media.ExtMediaManager.check,
        log_last_media_checkup, "before"
    )
    ccbc.collection._ExtCollection.emptyCids=wrap(
        ccbc.collection._ExtCollection.emptyCids,
        log_last_empty_card_checkup, "before"
    )
except:
    import anki
    anki.collection._Collection.fixIntegrity=wrap(
        anki.collection._Collection.fixIntegrity,
        log_last_db_checkup, "before"
    )
    anki.media.MediaManager.check=wrap(
        anki.media.MediaManager.check,
        log_last_media_checkup, "before"
    )
    anki.collection._Collection.emptyCids=wrap(
        anki.collection._Collection.emptyCids,
        log_last_empty_card_checkup, "before"
    )
