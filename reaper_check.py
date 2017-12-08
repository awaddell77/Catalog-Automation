#reaper new
from CatPickle import *
from w_csv import *
def reaper_check(fname):
    data = dictionarify(fname)
    skus = CatPickle(dir = "C:\\Users\Owner\\Catalog-Automation\\Pickles\\", fname="reaper.p")
    new_items = []
    for i in data:
        if i["Itemcode"] not in skus:
            skus.append(i["Itemcode"].strip())
            new_items.append(list(i.values()))
    print("Found {0} new items".format(len(new_items)))
    w_csv(new_items,"reapers.csv")
    return new_items
def reaper_add(fname):
    data = dictionarify(fname)
    skus = []
    for i in data:
        skus.append(i["Itemcode"].strip())
    pObj = CatPickle(dir = "C:\\Users\Owner\\Catalog-Automation\\Pickles\\", fname="reaper.p" )
    pObj.save_obj(skus)
