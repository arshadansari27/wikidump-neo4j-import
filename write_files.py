from parse import insert_entity
import sys
import json
import uuid
import codecs

FOLDER = 'CSVS/'


def print_no_newline(string):
    sys.stdout.write('\r')
    sys.stdout.write(string)
    sys.stdout.flush()

#codecs.open(FOLDER + 'reference.csv', 'w', encoding='utf-8') as reference_csv, \
#codecs.open(FOLDER + 'claim_reference_edge.csv', 'w', encoding='utf-8') as claim_reference_edge,\
#codecs.open(FOLDER + 'reference_property_edge.csv', 'w', encoding='utf-8') as reference_property_edge,\
#codecs.open(FOLDER + 'reference_entity_edge.csv', 'w', encoding='utf-8') as reference_entity_edge:

with codecs.open(FOLDER + 'entity.csv', 'w', encoding='utf-8') as entity_csv, \
        codecs.open(FOLDER + 'claims.csv', 'w', encoding='utf-8') as claims_csv,\
        codecs.open(FOLDER + 'qualifier.csv', 'w', encoding='utf-8') as qualifier_csv, \
        codecs.open(FOLDER + 'qualifier_property.csv', 'w', encoding='utf-8') as qualifier_property_edge,\
        codecs.open(FOLDER + 'entity_claim.csv', 'w', encoding='utf-8') as entity_claim_edge,\
        codecs.open(FOLDER + 'claim_property.csv', 'w', encoding='utf-8') as claim_property_edge,\
        codecs.open(FOLDER + 'claim_qualifier.csv', 'w', encoding='utf-8') as claim_qualifier_edge,\
        codecs.open(FOLDER + 'qualifier_entity.csv','w', encoding='utf-8') as qualifier_entity_edge:

    entity_csv.write("entityId:ID(Entity),name,description\n") 
    claims_csv.write("claimId:ID(Claim),property,type,value,rank\n")
    qualifier_csv.write("qualifierId:ID(Qualifier),property,type,value\n")
    entity_claim_edge.write(":START_ID(Entity),:END_ID(Claim)\n")
    claim_property_edge.write(":START_ID(Claim),:END_ID(Entity)\n")
    claim_qualifier_edge.write(":START_ID(Claim),:END_ID(Qualifier)\n")
    qualifier_property_edge.write(":START_ID(Qualifier),:END_ID(Entity)\n")
    qualifier_entity_edge.write(":START_ID(Qualifier),:END_ID(Entity)\n")


    PROPERTIES = []
    PROPERTIES = dict((u['id'], u) for u in PROPERTIES)

    def normalize(text):
        if not text or len(text) is '':
            return 'NULL'
        return text.replace(',', '').replace('\\', '').replace('"', '')
    
    def get_property(obj):
        return obj['property']

    def write_entity(entity):
        entity_csv.write("%s,%s,%s\n" % (entity['id'], normalize(entity['name']), normalize(entity['description'])))
        if entity.get('claims'):
            write_claim(entity['id'], entity['claims'])


    def write_claim(entity_id, claims):
        for _claims in claims:
            claim = _claims['claim']
            cid = claim['id']
            if not cid:
                continue
            cproperty = get_property(claim)
            if not cproperty:
                continue
            ctype = claim.get('type')
            if not ctype:
                ctype = 'NULL'
            cval = claim.get('value')
            if not cval:
                cval = 'NULL'
            else:
                cval = normalize(cval)
            crank = claim.get('rank')
            if not crank:
                crank = 'NULL'
            claims_csv.write("%s,%s,%s,%s,%s\n" % (claim['id'], get_property(claim), ctype, cval, crank))
            entity_claim_edge.write("%s,%s\n" % (entity_id, claim['id']))
            claim_property_edge.write("%s,%s\n" % (claim['id'], claim['property']))
            if _claims.get('qualifiers', []):
                for qualifier in _claims['qualifiers']:
                    qquid = uuid.uuid4()
                    claim_qualifier_edge.write("%s,%s\n" % (claim['id'], qquid))
                    if not qualifier.get('property'):
                        continue
                    qtype = qualifier.get('type')
                    if not qtype:
                        qtype = 'NULL'
                    qval = qualifier.get('value')
                    if not qval:
                        qval = 'NULL'
                    else:
                        qval = normalize(qval)
                    qualifier_property_edge.write("%s,%s\n" % (qquid, qualifier['property']))
                    qualifier_csv.write("%s,%s,%s,%s\n" % (qquid, get_property(qualifier), qtype, qval))
                    if qualifier['type'] == 'REF':
                        qualifier_entity_edge.write("%s,%s\n" % (qquid, qval))
            '''
            if _claims.get('references', []):
                for reference in _claims['references']:
                    rquid = uuid.uuid4()
                    claim_reference_edge.write("%s,%s\n" % (claim['id'], rquid))
                    reference_property_edge.write("%s,%s\n" % (rquid, reference['property']))
                    reference_csv.write("%s,%s,%s,%s,%s\n" % (rquid, get_property(reference), reference['type'], reference['value'].replace(',', ''), reference['order']))
                    if reference['type'] == 'REF':
                        reference_entity_edge.write("%s,%s\n" % (rquid, reference['value']))
            ''' 
   
    count = 0
    for line in sys.stdin:
        line = line.strip()
        if len(line) <= 1:
            continue
        if line[-1] == ',':
            line = line[:-1]
        data = insert_entity(line)
        count += 1
        if count % 10000 is 0:
            print_no_newline("%d" % count)
        if not data:
            continue
        write_entity(data)
    print_no_newline("%d\n" % count)
    entity_csv.write("\n") 
    claims_csv.write("\n")
    qualifier_csv.write("\n")
    #reference_csv.write("\n")
    entity_claim_edge.write("\n")
    claim_property_edge.write("\n")
    claim_qualifier_edge.write("\n")
    #claim_reference_edge.write("\n")
    qualifier_property_edge.write("\n")
    #reference_property_edge.write("\n")
    qualifier_entity_edge.write("\n")
    #reference_entity_edge.write("\n")

