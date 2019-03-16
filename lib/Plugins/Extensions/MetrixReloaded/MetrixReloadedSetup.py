from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label

from Tools import Notifications


# GUI (Components)
from Components.ActionMap import ActionMap

import os
import logging


class MetrixReloadedSetup(Screen):

    skin = """
<screen position="130,150" size="460,150" title="Ihad.tv e2-tutorial
lesson 2" >
<widget name="myLabel" position="10,60" size="200,40"
font="Regular;20"/>
</screen>"""

    def __init__(self, session, args=None):

        self.session = session
        Screen.__init__(self, session)

        self.log = self.initializeLog()
        self.log.info("MetrixReloadedSetup open")

        try:
            self["myLabel"] = Label(_("please press OK"))
            # Define Actions
            self["myActionsMap"] = ActionMap(["SetupActions", "ColorActions"],
                                             {
                "ok": self.myMsg,
                "cancel": self.close,
            }, -1)

        except Exception as e:
            self.log.exception("MetrixReloadedSetup: %s", str(e))
            self.close()

    def myMsg(self):
        self.session.open(MessageBox, _("Hello World!"), MessageBox.TYPE_INFO)

    def initializeLog(self):
        logger = logging.getLogger("MetrixReloadedSetup")
        logger.setLevel(logging.DEBUG)

        # create a file handler
        dir = '/mnt/hdd/MetrixReloaded/log/'

        if not os.path.exists(dir):
            os.makedirs(dir)

        handler = logging.FileHandler('%sMetrixReloadedSetup.log' % (dir))
        handler.setLevel(logging.DEBUG)

        # create a logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s: [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

        return logger
