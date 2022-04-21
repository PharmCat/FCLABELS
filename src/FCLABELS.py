__author__ =  'PharmCat'
__version__=  '1.2.2'

try:
    import csv, os, codecs, io
    from math import exp, floor
except:
    print("""This module requires csv, os, codecs, io and math modules.
			  One or more was not found.
              Please download these and try again""")
    raise ImportError

try:
    import spss, SpssClient, extension
except:
    # nontranslatable messages...
    print("""This module requires the spss, SpssClient and extension modules from
              SPSS Developer Central, www.spss.com/devcentral.  One or more was not found.
              Please download these and try again""")
    raise ImportError

from extension import Template, Syntax, processcmd

def Run(args):
	oobj = Syntax([
		Template("FILE", subc="", ktype="str", var="file"),
		Template("ID", subc="", ktype="str", var="id"),
		Template("LABELS", subc="", ktype="str", var="label")])
	args = args[list(args)[0]] ## Python 3!!!
	processcmd(oobj, args, action)

def action(file, id, label):

	SpssClient.StartClient();
	table=[];
	id_num = 0;
	labels_num = 1;
	labcnt = 0;
	header = True;
	#with open(file, 'rU') as f:
	#with io.open(file, 'rU', encoding='utf8') as f:
	with codecs.open(file, 'rU', encoding='utf8') as f:
		#reader = csv.reader(f, delimiter=';')
		reader = csv.reader(f)
		if header:
			table.append(next(reader))
		else:
			headerRaw = next(reader)
		for raw in reader:
			table.append(raw)
    #id = str.lower(str(id_));
    #label = str.lower(str(label_));
	#for cs in list(map(str.lower,  table[0])):
	#	print(cs + "; ");
	print( "Table columns number: ", str(len(table[0])));
    #for i in map(str.lower,  table[0]):
	#	print(i, " ");

    #id = str.lower(str(id)).strip();
    #label = str.lower(str(label)).strip();
	print( "Try to find columns '", str(id), "' and '", str(label), "'.");
	if str(id) in list(map(str.lower,  table[0])):
		for i in range(0, len(table[0])):
			if str.lower(table[0][i]) == str(id):
				id_num = i;
				print( "Column ID found ("+str(i)+").");
	else:
		print( "ID (",str(id) ,") not found.");
	if str(label) in list(map(str.lower,  table[0])):
		for i in range(0, len(table[0])):
			if str.lower(table[0][i]) == str(label):
				labels_num = i;
				print( "Column LABELS found ("+str(i)+").");
	else:
		print( "LABELS not found.");
	labcnt = len(table);

	print( "ID column N: ", str(id_num), "; LABELS column N: ", str(labels_num), ".");
	print( "Labels number: ", str(len(table)), ".");
#	for i in range(0, len(table)):
#		print table[i];

	spss.StartDataStep();
	set = spss.Dataset ();
	varcnt = spss.GetVariableCount();
	print("Variable count:" + str(varcnt));
	varlist=[];
	for i in range(varcnt):
		varlist.append(spss.GetVariableName(i));
	#print(varlist)
	chlistr=[]
	chlistc=[]
	#print(table)
	for i in range(0, varcnt):
		#print(varlist[i]);
		for k in range(0, labcnt):
                                                                        #print("Variable "+str(varlist[i])+" have description...");
			if varlist[i] == table[k][id_num].strip():
				#print("Variable "+str(varlist[i])+" have description...");
				s = table[k][labels_num].strip();
				n = table[k][id_num]
				set.varlist[i].label = s;
				#set.varlist[i].label = str(table[k][labels_num].strip());
				chlistr.append (n);
				chlistc.append (s);
				break;

	spss.EndDataStep();
	SpssClient.StopClient();
	spss.StartProcedure("Variable labels");
	table1 = spss.BasePivotTable("Variable labels", "Label");
	table1.SimplePivotTable(rowdim = "Variable",
	rowlabels = chlistr,
	#coldim = "Labels",
	collabels = ["Labels"],
	cells = chlistc);
	spss.EndProcedure();
	return;


def printlabels (csv):
	for i in range(csv):
		print(csv[0]);
