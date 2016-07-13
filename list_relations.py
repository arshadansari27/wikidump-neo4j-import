import os

with open('import.sh', 'w') as outfile:
    text = "neo4j-import --into graph.db --stacktrace --id-type string"
    fullpath = '/home/arshad/sandbox/conspiracy/CSVS'
    dirs = os.listdir(fullpath)
    text += ' '
    nodes = ["--nodes:%s %s/%s" % (d.replace('.csv', '').capitalize(), fullpath, d) for d in dirs if '_' not in d]
    text += ' '.join(nodes)
    text += ' '
    relationships = ["--relationships:%s %s/%s" % (d.replace('.csv', '').upper(), fullpath, d) for d in dirs if '_' in d]
    text += ' '.join(relationships)
    text += '\n'
    outfile.write(text)
