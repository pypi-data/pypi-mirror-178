import os

def arch():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'ARCH_AIC.txt')
    with open(filename, encoding="utf-8") as hw:
        print(hw.read())

def intro():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Intro.txt')
    with open(filename, encoding="utf-8") as hw:
        print(hw.read())

def models():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'models.txt')
    with open(filename, encoding="utf-8") as hw:
        print(hw.read())

def testplots():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'tests_plots.txt')
    with open(filename, encoding="utf-8") as hw:
        print(hw.read())

def tscode():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'TS_code.txt')
    with open(filename, encoding="utf-8") as hw:
        print(hw.read())

def getdocpath():
    dirname = os.path.dirname(__file__)
    print(dirname)


# arch()
# intro()
# models()
# testplots()
# tscode()
# getdocpath()

