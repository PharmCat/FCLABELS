__author__ =  'PharmCat'
__version__=  '1.2.0'

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

#args = args[args.keys()[0]]
#args = args[list(args)[0]]
#args = args["FCLABELS"]


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
		reader = csv.reader(f, delimiter=';')
		if header:
			table.append(next(reader))
		else:
			headerRaw = next(reader)
		for raw in reader:
			table.append(raw)

	for i in range(0, len(table[0])):
		#print(str(i))
		if table[0][i] == id:
			id_num = i;
		elif table[0][i] == label:
			labels_num = i;
	labcnt = len(table);

	print( "ID column N: " + str(id_num)+ "; LABELS column N: " + str(labels_num));
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
