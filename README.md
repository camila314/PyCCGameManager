## A small program to help with Geometry Dash data files
This package lets you manage your CCLocalLevels and CCGameManager files very easily. You can open up project files, edit them, inject levels into them, and save them.

An example program:

    >>>import CCManager
    >>>manager = CCManager.newManager()
    >>>levelData = open("leveldata.txt","r").read()
    >>>manager.injectLevel(levelData,levelName="Test Level",levelDesc="Cool level")
    >>>manager.save()

Credit goes to cos8o and Absolute for the Mac/Windows encode and decode algorithms. Also credit to JohnP55 for the level inject function