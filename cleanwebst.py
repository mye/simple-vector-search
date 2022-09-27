import json, sys
from html5_parser import parse

# given a parent node p and a class name c, provide a list of texts from div.c children
classdivs = lambda p, c: [''.join(e.itertext()) for e in p.xpath(f'//div[@class="{c}"]')]

# get all text in a node as a flat list
nodetexts = lambda n, cs: [text.strip() for elem in (classdivs(n, c) for c in cs) for text in elem]

# get a list of definitions text for relevant dictionary entries
divdefs = lambda n: nodetexts(n, ('def', 'q', 'ety', 'cs', 'note'))


if __name__ == '__main__':
	webst = json.load(sys.stdin)

	webst_clean = {entry.lower(): defs
		for entry in webst
		if (defs := divdefs(parse(webst[entry]))) # skip empty defs
	}

	json.dump(webst_clean, sys.stdout, sort_keys=True, indent=4)
