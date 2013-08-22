import cPickle

listdeepest1 = [1,2,3,4];
listdeepest2 = ["hi", "bye"];
listmiddle1 = [listdeepest1, listdeepest2];
listmiddle2 = [10, 20];
listtop = [listmiddle1, listmiddle2];
pickle_file = open("pickle_file.dat", "w");
cPickle.dump(listtop, pickle_file, protocol=0);
pickle_file = open("pickle_file.dat", "r");
newlist = cPickle.load(pickle_file);
newlist[0][0][2] = "someting else";
print listmiddle1
print newlist
print listtop