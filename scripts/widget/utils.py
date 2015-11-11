__author__ = "Zhiping Luo"
__contact__ = "luozhipi@gmail.com"
__website__ = "luozhipi.github.io"

import os
import sys

from PySide.QtCore import Slot, QMetaObject
from PySide.QtUiTools import QUiLoader
from PySide.QtGui import QApplication, QMainWindow, QMessageBox


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

#----------------------------------------------------------------------
def findAllFiles(fileDirectory, fileExtension):
    """
    Args:
      fileDirectory (str)
      fileExtension (str)

    Returns:
      list
    """
    return [f for f in os.listdir(fileDirectory) if f.lower().endswith(fileExtension)]

#----------------------------------------------------------------------
def findAllModules():
    """
    Returns:
      list
    """
    allPyFiles = findAllFiles(SCRIPT_DIRECTORY, ".py")
    return [f.split('.')[0] for f in allPyFiles if not f.startswith("__init__")]

#----------------------------------------------------------------------
def findAllTabs():
    """
    Returns:
      list
    """
    tabModules = []
    for m in findAllModules():
        mod = __import__("widget.%s" % m, '', '', [m])
        if hasattr(mod, 'TAB') and mod.ENABLE:
            reload(mod)
            tabModules.append(mod)
            
    tabModules.sort(key=lambda m: m.INDEX)
    return [m.getTab() for m in tabModules]

#----------------------------------------------------------------------
class UiLoader(QUiLoader):
    """
    Subclass :class:`~PySide.QtUiTools.QUiLoader` to create the user interface
    in a base instance.

    Unlike :class:`~PySide.QtUiTools.QUiLoader` itself this class does not
    create a new instance of the top-level widget, but creates the user
    interface in an existing instance of the top-level class.

    This mimics the behaviour of :func:`PyQt4.uic.loadUi`.
    """

    def __init__(self, baseinstance):
        """
        Create a loader for the given ``baseinstance``.

        The user interface is created in ``baseinstance``, which must be an
        instance of the top-level class in the user interface to load, or a
        subclass thereof.

        ``parent`` is the parent object of this loader.
        """
        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            # supposed to create the top-level widget, return the base instance
            # instead
            return self.baseinstance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.baseinstance:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.baseinstance, name, widget)
            return widget


def loadUi(uifile, baseinstance=None):
    """
    Dynamically load a user interface from the given ``uifile``.

    ``uifile`` is a string containing a file name of the UI file to load.

    If ``baseinstance`` is ``None``, the a new instance of the top-level widget
    will be created.  Otherwise, the user interface is created within the given
    ``baseinstance``.  In this case ``baseinstance`` must be an instance of the
    top-level widget class in the UI file to load, or a subclass thereof.  In
    other words, if you've created a ``QMainWindow`` interface in the designer,
    ``baseinstance`` must be a ``QMainWindow`` or a subclass thereof, too.  You
    cannot load a ``QMainWindow`` UI file with a plain
    :class:`~PySide.QtGui.QWidget` as ``baseinstance``.

    :method:`~PySide.QtCore.QMetaObject.connectSlotsByName()` is called on the
    created user interface, so you can implemented your slots according to its
    conventions in your widget class.

    Return ``baseinstance``, if ``baseinstance`` is not ``None``.  Otherwise
    return the newly created instance of the user interface.
    """
    loader = UiLoader(baseinstance)
    widget = loader.load(uifile)
    QMetaObject.connectSlotsByName(widget)
    return widget


def main():
    app = QApplication(sys.argv)
    app.exec_()


if __name__ == '__main__':
    main()
