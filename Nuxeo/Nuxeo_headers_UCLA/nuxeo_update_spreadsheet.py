import unicodecsv as csv
import os 
try:
    filepath = raw_input('Enter Nuxeo File Path: ') 
except:
    filepath = input('Enter Nuxeo File Path: ') 
try:
    choice = raw_input('Object Level (ENTER O) or Item Level (ENTER I): ')
except:
    choice = input('Object Level (ENTER O) or Item Level (ENTER I): ')
try:
    url = raw_input('Enter Google Sheet URL: ')
except:
    url = input('Enter Google Sheet URL: ')
from pynux import utils

def object_level(filepath):
    nx = utils.Nuxeo()
    data = []
    for n in nx.children(filepath):
        data2 = {}
        data2['File path'] = n['path']
        data2['Title'] = n['properties']['dc:title']
        if n['properties']['ucldc_schema:type'] != None and n['properties']['ucldc_schema:type'] != '':
            data2['Type'] = n['properties']['ucldc_schema:type']
        altnumb = 0
        if type(n['properties']['ucldc_schema:alternativetitle']) == list and len(n['properties']['ucldc_schema:alternativetitle']) > 0:
            while altnumb < len(n['properties']['ucldc_schema:alternativetitle']):
                numb = altnumb + 1
                name = 'Alternative Title %d' % numb
                data2[name]= n['properties']['ucldc_schema:alternativetitle'][altnumb]
                altnumb += 1
        if n['properties']['ucldc_schema:identifier'] != None and n['properties']['ucldc_schema:identifier'] != '':
            data2['Identifier'] = n['properties']['ucldc_schema:identifier']
        locnumb = 0
        if type(n['properties']['ucldc_schema:localidentifier']) == list and len(n['properties']['ucldc_schema:localidentifier']) > 0:
            while locnumb < len(n['properties']['ucldc_schema:localidentifier']):
                numb = locnumb + 1
                name = 'Local Identifier %d' % numb
                data2[name]= n['properties']['ucldc_schema:localidentifier'][locnumb]
                locnumb += 1
        
        campnumb = 0
        if type(n['properties']['ucldc_schema:campusunit']) == list and len(n['properties']['ucldc_schema:campusunit']) > 0:
            while campnumb < len(n['properties']['ucldc_schema:campusunit']):
                numb = campnumb + 1
                name = 'Campus/Unit %d' % numb
                data2[name]= n['properties']['ucldc_schema:campusunit'][campnumb]
                campnumb += 1
       
        datenumb = 0
        if type(n['properties']['ucldc_schema:date']) == list and len(n['properties']['ucldc_schema:date']) > 0:
            while datenumb < len(n['properties']['ucldc_schema:date']):
                numb = datenumb + 1
                try: 
                    name = 'Date %d' % numb
                    if n['properties']['ucldc_schema:date'][datenumb]['date'] != None and n['properties']['ucldc_schema:date'][datenumb]['date'] != '':
                        data2[name] = n['properties']['ucldc_schema:date'][datenumb]['date']
                except:
                    pass
                try: 
                    name = 'Date %d Type' % numb
                    if n['properties']['ucldc_schema:date'][datenumb]['datetype'] != None and n['properties']['ucldc_schema:date'][datenumb]['datetype'] != '':
                        data2[name] = n['properties']['ucldc_schema:date'][datenumb]['datetype']
                except:
                    pass
                try:
                    name = 'Date %d Inclusive Start' % numb
                    if n['properties']['ucldc_schema:date'][datenumb]['inclusivestart'] != None and n['properties']['ucldc_schema:date'][datenumb]['inclusivestart'] != '':
                        data2[name] = n['properties']['ucldc_schema:date'][datenumb]['inclusivestart']
                except:
                    pass
                try:
                    name = 'Date %d Inclusive End' % numb
                    if n['properties']['ucldc_schema:date'][datenumb]['inclusiveend'] != None and n['properties']['ucldc_schema:date'][datenumb]['inclusiveend'] != '':
                        data2[name] = n['properties']['ucldc_schema:date'][datenumb]['inclusiveend']
                except:
                    pass
                try:
                    name = 'Date %d Single' % numb
                    if n['properties']['ucldc_schema:date'][datenumb]['single'] != None and n['properties']['ucldc_schema:date'][datenumb]['single'] != '':
                        data2[name] = n['properties']['ucldc_schema:date'][datenumb]['single']
                except:
                    pass
                datenumb += 1
 
        pubnumb = 0
        if type(n['properties']['ucldc_schema:publisher']) == list and len(n['properties']['ucldc_schema:publisher']) > 0:
            while pubnumb < len(n['properties']['ucldc_schema:publisher']):
                numb = pubnumb + 1
                name = 'Publication/Origination Info %d' % numb
                data2[name]= n['properties']['ucldc_schema:publisher'][pubnumb]
                pubnumb += 1
                
        creatnumb = 0
        if type(n['properties']['ucldc_schema:creator']) == list and len(n['properties']['ucldc_schema:creator']) > 0:
            while creatnumb < len(n['properties']['ucldc_schema:creator']):
                numb = creatnumb + 1
                try: 
                    name = 'Creator %d Name' % numb
                    if n['properties']['ucldc_schema:creator'][creatnumb]['name'] != None and n['properties']['ucldc_schema:creator'][creatnumb]['name'] != '':
                        data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['name']
                except:
                    pass
                try: 
                    name = 'Creator %d Name Type' % numb
                    if n['properties']['ucldc_schema:creator'][creatnumb]['nametype'] != None and n['properties']['ucldc_schema:creator'][creatnumb]['nametype'] != '':
                        data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['nametype']
                except:
                    pass
                try:
                    name = 'Creator %d Role' % numb
                    if n['properties']['ucldc_schema:creator'][creatnumb]['role'] != None and n['properties']['ucldc_schema:creator'][creatnumb]['role'] != '':
                        data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['role']
                except:
                    pass
                try:
                    name = 'Creator %d Source' % numb
                    if n['properties']['ucldc_schema:creator'][creatnumb]['source'] != None and n['properties']['ucldc_schema:creator'][creatnumb]['source'] != '':
                        data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['source']
                except:
                    pass
                try:
                    name = 'Creator %d Authority ID' % numb
                    if n['properties']['ucldc_schema:creator'][creatnumb]['authorityid'] != None and n['properties']['ucldc_schema:creator'][creatnumb]['authorityid'] != '':
                        data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['authorityid']
                except:
                    pass
                creatnumb += 1
        
        contnumb = 0
        if type(n['properties']['ucldc_schema:contributor']) == list and len(n['properties']['ucldc_schema:contributor']) > 0:
            while contnumb < len(n['properties']['ucldc_schema:contributor']):
                numb = contnumb + 1
                try: 
                    name = 'Contributor %d Name' % numb
                    if n['properties']['ucldc_schema:contributor'][contnumb]['name'] != None and n['properties']['ucldc_schema:contributor'][contnumb]['name'] != '':
                        data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['name']
                except:
                    pass
                try: 
                    name = 'Contributor %d Name Type' % numb
                    if n['properties']['ucldc_schema:contributor'][contnumb]['nametype'] != None and n['properties']['ucldc_schema:contributor'][contnumb]['nametype'] != '':
                        data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['nametype']
                except:
                    pass
                try:
                    name = 'Contributor %d Role' % numb
                    if n['properties']['ucldc_schema:contributor'][contnumb]['role'] != None and n['properties']['ucldc_schema:contributor'][contnumb]['role'] != '':
                        data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['role']
                except:
                    pass
                try:
                    name = 'Contributor %d Source' % numb
                    if n['properties']['ucldc_schema:contributor'][contnumb]['source'] != None and n['properties']['ucldc_schema:contributor'][contnumb]['source'] != '':
                        data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['source']
                except:
                    pass
                try:
                    name = 'Contributor %d Authority ID' % numb
                    if n['properties']['ucldc_schema:contributor'][contnumb]['authorityid'] != None and n['properties']['ucldc_schema:contributor'][contnumb]['authorityid'] != '':
                        data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['authorityid']
                except:
                    pass
                contnumb += 1
                
        if n['properties']['ucldc_schema:physdesc'] != None and n['properties']['ucldc_schema:physdesc'] != '':
            data2['Format/Physical Description'] = n['properties']['ucldc_schema:physdesc']
            
        descnumb = 0
        if type(n['properties']['ucldc_schema:description']) == list and len(n['properties']['ucldc_schema:description']) > 0:
            while descnumb < len(n['properties']['ucldc_schema:description']):
                numb = descnumb + 1
                try:
                    name = "Description %d Note" % numb
                    if n['properties']['ucldc_schema:description'][descnumb]['item'] != None and n['properties']['ucldc_schema:description'][descnumb]['item'] != '':
                        data2[name] = n['properties']['ucldc_schema:description'][descnumb]['item']
                except:
                    pass
                try:
                    name = "Description %d Type" % numb
                    if n['properties']['ucldc_schema:description'][descnumb]['type'] != None and n['properties']['ucldc_schema:description'][descnumb]['type'] != '':
                        data2[name] = n['properties']['ucldc_schema:description'][descnumb]['type']
                except:
                    pass
                descnumb += 1
                
        if n['properties']['ucldc_schema:extent'] != None and n['properties']['ucldc_schema:extent'] != '':      
            data2['Extent'] = n['properties']['ucldc_schema:extent']
            
        langnumb = 0
        if type(n['properties']['ucldc_schema:language']) == list and len(n['properties']['ucldc_schema:language']) > 0:
            while langnumb < len(n['properties']['ucldc_schema:language']):
                numb = langnumb + 1
                try:
                    name = "Language %d" % numb
                    if n['properties']['ucldc_schema:language'][langnumb]['language'] != None and n['properties']['ucldc_schema:language'][langnumb]['language'] != '':
                        data2[name] = n['properties']['ucldc_schema:language'][langnumb]['language']
                except:
                    pass
                try:
                    name = "Language %d Code" % numb
                    if n['properties']['ucldc_schema:language'][langnumb]['code'] != None and n['properties']['ucldc_schema:language'][langnumb]['code'] != '':
                        data2[name] = n['properties']['ucldc_schema:language'][langnumb]['code']
                except:
                    pass
                langnumb += 1
        
        tempnumb = 0
        if type(n['properties']['ucldc_schema:temporalcoverage']) == list and len(n['properties']['ucldc_schema:temporalcoverage']) > 0:
            while tempnumb < len(n['properties']['ucldc_schema:temporalcoverage']):
                numb = tempnumb + 1
                name = 'Temporal Coverage %d' % numb
                data2[name]= n['properties']['ucldc_schema:temporalcoverage'][tempnumb]
                tempnumb += 1

        if n['properties']['ucldc_schema:transcription'] != None and n['properties']['ucldc_schema:transcription'] != '':
            data2['Transcription'] = n['properties']['ucldc_schema:transcription']
        if n['properties']['ucldc_schema:accessrestrict'] != None and n['properties']['ucldc_schema:accessrestrict'] != '':
            data2['Access Restrictions'] = n['properties']['ucldc_schema:accessrestrict']
        if n['properties']['ucldc_schema:rightsstatement'] != None and n['properties']['ucldc_schema:rightsstatement'] != '':
            data2['Copyright Statement'] = n['properties']['ucldc_schema:rightsstatement']
        if n['properties']['ucldc_schema:rightsstatus'] != None and n['properties']['ucldc_schema:rightsstatus'] != '':
            data2['Copyright Status'] = n['properties']['ucldc_schema:rightsstatus']
        
        rightsnumb = 0
        if type(n['properties']['ucldc_schema:rightsholder']) == list and len(n['properties']['ucldc_schema:rightsholder']) > 0:
            while contnumb < len(n['properties']['ucldc_schema:rightsholder']):
                numb = contnumb + 1
                try: 
                    name = 'Copyright Holder %d Name' % numb
                    if n['properties']['ucldc_schema:rightsholder'][contnumb]['name'] != None and n['properties']['ucldc_schema:rightsholder'][contnumb]['name'] != '':
                        data2[name] = n['properties']['ucldc_schema:rightsholder'][contnumb]['name']
                except:
                    pass
                try: 
                    name = 'Copyright Holder %d Name Type' % numb
                    if n['properties']['ucldc_schema:rightsholder'][contnumb]['nametype'] != None and n['properties']['ucldc_schema:rightsholder'][contnumb]['nametype'] != '':
                        data2[name] = n['properties']['ucldc_schema:rightsholder'][contnumb]['nametype']
                except:
                    pass
                try:
                    name = 'Copyright Holder %d Source' % numb
                    if n['properties']['ucldc_schema:rightsholder'][contnumb]['source'] != None and n['properties']['ucldc_schema:rightsholder'][contnumb]['source'] != '':
                        data2[name] = n['properties']['ucldc_schema:rightsholder'][contnumb]['source']
                except:
                    pass
                try:
                    name = 'Copyright Holder %d Authority ID' % numb
                    if n['properties']['ucldc_schema:rightsholder'][contnumb]['authorityid'] != None and n['properties']['ucldc_schema:rightsholder'][contnumb]['authorityid'] != '':
                        data2[name] = n['properties']['ucldc_schema:rightsholder'][contnumb]['authorityid']
                except:
                    pass
                contnumb += 1
       
        if n['properties']['ucldc_schema:rightscontact'] != None and n['properties']['ucldc_schema:rightscontact'] != '':
            data2['Copyright Contact'] = n['properties']['ucldc_schema:rightscontact']
        if n['properties']['ucldc_schema:rightsnotice'] != None and n['properties']['ucldc_schema:rightsnotice'] != '':
            data2['Copyright Notice'] = n['properties']['ucldc_schema:rightsnotice']
        if n['properties']['ucldc_schema:rightsdeterminationdate'] != None and n['properties']['ucldc_schema:rightsdeterminationdate'] != '':
            data2['Copyright Determination Date'] = n['properties']['ucldc_schema:rightsdeterminationdate']
        if n['properties']['ucldc_schema:rightsstartdate'] != None and n['properties']['ucldc_schema:rightsstartdate'] != '':
            data2['Copyright Start Date'] = n['properties']['ucldc_schema:rightsstartdate']
        if n['properties']['ucldc_schema:rightsenddate'] != None and n['properties']['ucldc_schema:rightsenddate'] != '':
            data2['Copyright End Date'] = n['properties']['ucldc_schema:rightsenddate']
        if n['properties']['ucldc_schema:rightsjurisdiction'] != None and n['properties']['ucldc_schema:rightsjurisdiction'] != '':
            data2['Copyright Jurisdiction'] = n['properties']['ucldc_schema:rightsjurisdiction']
        if n['properties']['ucldc_schema:rightsnote'] != None and n['properties']['ucldc_schema:rightsnote'] != '':
            data2['Copyright Note'] = n['properties']['ucldc_schema:rightsnote']
            
        collnumb = 0
        if type(n['properties']['ucldc_schema:collection']) == list and len(n['properties']['ucldc_schema:collection']) > 0:
            while collnumb < len(n['properties']['ucldc_schema:collection']):
                numb = collnumb + 1
                name = 'Collection %d' % numb
                data2[name]= n['properties']['ucldc_schema:collection'][collnumb]
                collnumb += 1
                
        relnumb = 0
        if type(n['properties']['ucldc_schema:relatedresource']) == list and len(n['properties']['ucldc_schema:relatedresource']) > 0:
            while relnumb < len(n['properties']['ucldc_schema:relatedresource']):
                numb = relnumb + 1
                name = 'Related Resource %d' % numb
                data2[name]= n['properties']['ucldc_schema:relatedresource'][relnumb]
                relnumb += 1
                
        if n['properties']['ucldc_schema:source'] != None and n['properties']['ucldc_schema:source'] != '':
            data2['Source'] = n['properties']['ucldc_schema:source']
            
        subnumb = 0
        if type(n['properties']['ucldc_schema:subjectname']) == list and len(n['properties']['ucldc_schema:subjectname']) > 0:
            while subnumb < len(n['properties']['ucldc_schema:subjectname']):
                numb = subnumb + 1
                try: 
                    name = 'Subject (Name) %d Name' % numb
                    if n['properties']['ucldc_schema:subjectname'][subnumb]['name'] != None and n['properties']['ucldc_schema:subjectname'][subnumb]['name'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['name']
                except:
                    pass
                try: 
                    name = 'Subject (Name) %d Name Type' % numb
                    if n['properties']['ucldc_schema:subjectname'][subnumb]['name_type'] != None and n['properties']['ucldc_schema:subjectname'][subnumb]['name_type'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['name_type']
                except:
                    pass
                try:
                    name = 'Subject (Name) %d Role' % numb
                    if n['properties']['ucldc_schema:subjectname'][subnumb]['role'] != None and n['properties']['ucldc_schema:subjectname'][subnumb]['role'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['role']
                except:
                    pass
                try:
                    name = 'Subject (Name) %d Source' % numb
                    if n['properties']['ucldc_schema:subjectname'][subnumb]['source'] != None and n['properties']['ucldc_schema:subjectname'][subnumb]['source'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['source']
                except:
                    pass
                try:
                    name = 'Subject (Name) %d Authority ID' % numb
                    if n['properties']['ucldc_schema:subjectname'][subnumb]['authorityid'] != None and n['properties']['ucldc_schema:subjectname'][subnumb]['authorityid'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['authorityid']
                except:
                    pass
                subnumb += 1
       
        plcnumb = 0
        if type(n['properties']['ucldc_schema:place']) == list and len(n['properties']['ucldc_schema:place']) > 0:
            while plcnumb < len(n['properties']['ucldc_schema:place']):
                numb = plcnumb + 1
                try: 
                    name = 'Place %d Name' % numb
                    if n['properties']['ucldc_schema:place'][plcnumb]['name'] != None and n['properties']['ucldc_schema:place'][plcnumb]['name'] != '':
                        data2[name] = n['properties']['ucldc_schema:place'][plcnumb]['name']
                except:
                    pass
                try:
                    name = 'Place %d Coordinates' % numb
                    if n['properties']['ucldc_schema:place'][plcnumb]['coordinates'] != None and n['properties']['ucldc_schema:place'][plcnumb]['coordinates'] != '':
                        data2[name] = n['properties']['ucldc_schema:place'][plcnumb]['coordinates']
                except:
                    pass
                try:
                    name = 'Place %d Source' % numb
                    if n['properties']['ucldc_schema:place'][plcnumb]['source'] != None and n['properties']['ucldc_schema:place'][plcnumb]['source'] != '':
                        data2[name] = n['properties']['ucldc_schema:place'][plcnumb]['source']
                except:
                    pass
                try:
                    name = 'Place %d Authority ID' % numb
                    if n['properties']['ucldc_schema:place'][plcnumb]['authorityid'] != None and n['properties']['ucldc_schema:place'][plcnumb]['authorityid'] != '':
                        data2[name] = n['properties']['ucldc_schema:place'][plcnumb]['authorityid']
                except:
                    pass
                plcnumb += 1
        
        topnumb = 0
        if type(n['properties']['ucldc_schema:subjecttopic']) == list and len(n['properties']['ucldc_schema:subjecttopic']) > 0:
            while topnumb < len(n['properties']['ucldc_schema:subjecttopic']):
                numb = topnumb + 1
                try: 
                    name = 'Subject (Topic) %d Heading' % numb
                    if n['properties']['ucldc_schema:subjecttopic'][topnumb]['heading'] != None and n['properties']['ucldc_schema:subjecttopic'][topnumb]['heading'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjecttopic'][topnumb]['heading']
                except:
                    pass		
                try:
                    name = 'Subject (Topic) %d Heading Type' % numb
                    if n['properties']['ucldc_schema:subjecttopic'][topnumb]['headingtype'] != None and n['properties']['ucldc_schema:subjecttopic'][topnumb]['headingtype'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjecttopic'][topnumb]['headingtype']
                except:
                    pass
                try:
                    name = 'Subject (Topic) %d Source' % numb
                    if n['properties']['ucldc_schema:subjecttopic'][topnumb]['source'] != None and n['properties']['ucldc_schema:subjecttopic'][topnumb]['source'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjecttopic'][topnumb]['source']
                except:
                    pass
                try:
                    name = 'Subject (Topic) %d Authority ID' % numb
                    if n['properties']['ucldc_schema:subjecttopic'][topnumb]['authorityid'] != None and n['properties']['ucldc_schema:subjecttopic'][topnumb]['authorityid'] != '':
                        data2[name] = n['properties']['ucldc_schema:subjecttopic'][topnumb]['authorityid']
                except:
                    pass
                topnumb += 1
      
        formnumb = 0
        if type(n['properties']['ucldc_schema:formgenre']) == list and len(n['properties']['ucldc_schema:formgenre']) > 0:
            while formnumb < len(n['properties']['ucldc_schema:formgenre']):
                numb = formnumb + 1
                try: 
                    name = 'Form/Genre %d Heading' % numb
                    if n['properties']['ucldc_schema:formgenre'][formnumb]['heading'] != None and n['properties']['ucldc_schema:formgenre'][formnumb]['heading'] != '':
                        data2[name] = n['properties']['ucldc_schema:formgenre'][formnumb]['heading']
                except:
                    pass		
                try:
                    name = 'Form/Genre %d Source' % numb
                    if n['properties']['ucldc_schema:formgenre'][formnumb]['source'] != None and n['properties']['ucldc_schema:formgenre'][formnumb]['source'] != '':
                        data2[name] = n['properties']['ucldc_schema:formgenre'][formnumb]['source']
                except:
                    pass
                try:
                    name = 'Form/Genre %d Authority ID' % numb
                    if n['properties']['ucldc_schema:formgenre'][formnumb]['authorityid'] != None and n['properties']['ucldc_schema:formgenre'][formnumb]['authorityid'] != '':
                        data2[name] = n['properties']['ucldc_schema:formgenre'][formnumb]['authorityid']
                except:
                    pass
                formnumb += 1
       
        provnumb = 0
        if type(n['properties']['ucldc_schema:provenance']) == list and len(n['properties']['ucldc_schema:provenance']) > 0:
            while provnumb < len(n['properties']['ucldc_schema:provenance']):
                numb = provnumb + 1
                name = 'Provenance %d' % numb
                data2[name]= n['properties']['ucldc_schema:provenance'][provnumb]
                provnumb += 1
        
        if n['properties']['ucldc_schema:physlocation'] != None and n['properties']['ucldc_schema:physlocation'] != '':
            data2['Physical Location'] = n['properties']['ucldc_schema:physlocation']
        data.append(data2)

    fieldnames = []
    for data2 in data:
        for key, value in data2.items():
            fieldnames.append(key)
    fieldnames = list(set(fieldnames))
    fieldnames = sorted(fieldnames, reverse=True)
    
    return {'fieldnames':fieldnames, 'data':data, 'filename':"nuxeo_object_%s.tsv"%nx.get_metadata(path=filepath)['properties']['dc:title']}
    
    
def item_level(filepath):
    nx = utils.Nuxeo()
    data = []
    for n in nx.children(filepath):
        for x in nx.children(n['path']):
            data2 = {}
            data2['File path'] = x['path']
            data2['Title'] = x['properties']['dc:title']
            if x['properties']['ucldc_schema:type'] != None and x['properties']['ucldc_schema:type'] != '':
                data2['Type'] = x['properties']['ucldc_schema:type']
                
            altnumb = 0
            if type(x['properties']['ucldc_schema:alternativetitle']) == list and len(x['properties']['ucldc_schema:alternativetitle']) > 0:
                while altnumb < len(x['properties']['ucldc_schema:alternativetitle']):
                    numb = altnumb + 1
                    name = 'Alternative Title %d' % numb
                    data2[name]= x['properties']['ucldc_schema:alternativetitle'][altnumb]
                    altnumb += 1
            
            if x['properties']['ucldc_schema:identifier'] != None and x['properties']['ucldc_schema:identifier'] != '':
                data2['Identifier'] = x['properties']['ucldc_schema:identifier']
                
            locnumb = 0
            if type(x['properties']['ucldc_schema:localidentifier']) == list and len(x['properties']['ucldc_schema:localidentifier']) > 0:
                while locnumb < len(x['properties']['ucldc_schema:localidentifier']):
                    numb = locnumb + 1
                    name = 'Local Identifier %d' % numb
                    data2[name]= x['properties']['ucldc_schema:localidentifier'][locnumb]
                    locnumb += 1
            
            campnumb = 0
            if type(x['properties']['ucldc_schema:campusunit']) == list and len(x['properties']['ucldc_schema:campusunit']) > 0:
                while campnumb < len(x['properties']['ucldc_schema:campusunit']):
                    numb = campnumb + 1
                    name = 'Campus/Unit %d' % numb
                    data2[name]= x['properties']['ucldc_schema:campusunit'][campnumb]
                    campnumb += 1
            
            datenumb = 0
            if type(x['properties']['ucldc_schema:date']) == list and len(x['properties']['ucldc_schema:date']) > 0:
                while datenumb < len(x['properties']['ucldc_schema:date']):
                    numb = datenumb + 1
                    try: 
                        name = 'Date %d' % numb
                        if x['properties']['ucldc_schema:date'][datenumb]['date'] != None and x['properties']['ucldc_schema:date'][datenumb]['date'] != '':
                            data2[name] = x['properties']['ucldc_schema:date'][datenumb]['date']
                    except:
                        pass
                    try: 
                        name = 'Date %d Type' % numb
                        if x['properties']['ucldc_schema:date'][datenumb]['datetype'] != None and x['properties']['ucldc_schema:date'][datenumb]['datetype'] != '':
                            data2[name] = x['properties']['ucldc_schema:date'][datenumb]['datetype']
                    except:
                        pass
                    try:
                        name = 'Date %d Inclusive Start' % numb
                        if x['properties']['ucldc_schema:date'][datenumb]['inclusivestart'] != None and x['properties']['ucldc_schema:date'][datenumb]['inclusivestart'] != '':
                            data2[name] = x['properties']['ucldc_schema:date'][datenumb]['inclusivestart']
                    except:
                        pass
                    try:
                        name = 'Date %d Inclusive End' % numb
                        if x['properties']['ucldc_schema:date'][datenumb]['inclusiveend'] != None and x['properties']['ucldc_schema:date'][datenumb]['inclusiveend'] != '':
                            data2[name] = x['properties']['ucldc_schema:date'][datenumb]['inclusiveend']
                    except:
                        pass
                    try:
                        name = 'Date %d Single' % numb
                        if x['properties']['ucldc_schema:date'][datenumb]['single'] != None and x['properties']['ucldc_schema:date'][datenumb]['single'] != '':
                            data2[name] = x['properties']['ucldc_schema:date'][datenumb]['single']
                    except:
                        pass
                    datenumb += 1
           
            pubnumb = 0
            if type(x['properties']['ucldc_schema:publisher']) == list and len(x['properties']['ucldc_schema:publisher']) > 0:
                while pubnumb < len(x['properties']['ucldc_schema:publisher']):
                    numb = pubnumb + 1
                    name = 'Publication/Origination Info %d' % numb
                    data2[name]= x['properties']['ucldc_schema:publisher'][pubnumb]
                    pubnumb += 1
           
            creatnumb = 0
            if type(x['properties']['ucldc_schema:creator']) == list and len(x['properties']['ucldc_schema:creator']) > 0:
                while creatnumb < len(x['properties']['ucldc_schema:creator']):
                    numb = creatnumb + 1
                    try: 
                        name = 'Creator %d Name' % numb
                        if x['properties']['ucldc_schema:creator'][creatnumb]['name'] != None and x['properties']['ucldc_schema:creator'][creatnumb]['name'] != '':
                            data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['name']
                    except:
                        pass
                    try: 
                        name = 'Creator %d Name Type' % numb
                        if x['properties']['ucldc_schema:creator'][creatnumb]['nametype'] != None and x['properties']['ucldc_schema:creator'][creatnumb]['nametype'] != '':
                            data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['nametype']
                    except:
                        pass
                    try:
                        name = 'Creator %d Role' % numb
                        if x['properties']['ucldc_schema:creator'][creatnumb]['role'] != None and x['properties']['ucldc_schema:creator'][creatnumb]['role'] != '':
                            data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['role']
                    except:
                        pass
                    try:
                        name = 'Creator %d Source' % numb
                        if x['properties']['ucldc_schema:creator'][creatnumb]['source'] != None and x['properties']['ucldc_schema:creator'][creatnumb]['source'] != '':
                            data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['source']
                    except:
                        pass
                    try:
                        name = 'Creator %d Authority ID' % numb
                        if x['properties']['ucldc_schema:creator'][creatnumb]['authorityid'] != None and x['properties']['ucldc_schema:creator'][creatnumb]['authorityid'] != '':
                            data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['authorityid']
                    except:
                        pass
                    creatnumb += 1
           
            contnumb = 0
            if type(x['properties']['ucldc_schema:contributor']) == list and len(x['properties']['ucldc_schema:contributor']) > 0:
                while contnumb < len(x['properties']['ucldc_schema:contributor']):
                    numb = contnumb + 1
                    try: 
                        name = 'Contributor %d Name' % numb
                        if x['properties']['ucldc_schema:contributor'][contnumb]['name'] != None and x['properties']['ucldc_schema:contributor'][contnumb]['name'] != '':
                            data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['name']
                    except:
                        pass
                    try: 
                        name = 'Contributor %d Name Type' % numb
                        if x['properties']['ucldc_schema:contributor'][contnumb]['nametype'] != None and x['properties']['ucldc_schema:contributor'][contnumb]['nametype'] != '':
                            data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['nametype']
                    except:
                        pass
                    try:
                        name = 'Contributor %d Role' % numb
                        if x['properties']['ucldc_schema:contributor'][contnumb]['role'] != None and x['properties']['ucldc_schema:contributor'][contnumb]['role'] != '':
                            data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['role']
                    except:
                        pass
                    try:
                        name = 'Contributor %d Source' % numb
                        if x['properties']['ucldc_schema:contributor'][contnumb]['source'] != None and x['properties']['ucldc_schema:contributor'][contnumb]['source'] != '':
                            data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['source']
                    except:
                        pass
                    try:
                        name = 'Contributor %d Authority ID' % numb
                        if x['properties']['ucldc_schema:contributor'][contnumb]['authorityid'] != None and x['properties']['ucldc_schema:contributor'][contnumb]['authorityid'] != '':
                            data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['authorityid']
                    except:
                        pass
                    contnumb += 1
            
            if x['properties']['ucldc_schema:physdesc'] != None and x['properties']['ucldc_schema:physdesc'] != '':
                data2['Format/Physical Description'] = x['properties']['ucldc_schema:physdesc']
                
            descnumb = 0
            if type(x['properties']['ucldc_schema:description']) == list and len(x['properties']['ucldc_schema:description']) > 0:
                while descnumb < len(x['properties']['ucldc_schema:description']):
                    numb = descnumb + 1
                    try:
                        name = "Description %d Note" % numb
                        if x['properties']['ucldc_schema:description'][descnumb]['item'] != None and x['properties']['ucldc_schema:description'][descnumb]['item'] != '':
                            data2[name] = x['properties']['ucldc_schema:description'][descnumb]['item']
                    except:
                        pass
                    try:
                        name = "Description %d Type" % numb
                        if x['properties']['ucldc_schema:description'][descnumb]['type'] != None and x['properties']['ucldc_schema:description'][descnumb]['type'] != '':
                            data2[name] = x['properties']['ucldc_schema:description'][descnumb]['type']
                    except:
                        pass
                    descnumb += 1
           
            if x['properties']['ucldc_schema:extent'] != None and x['properties']['ucldc_schema:extent'] != '':
                data2['Extent'] = x['properties']['ucldc_schema:extent']
                
            langnumb = 0
            if type(x['properties']['ucldc_schema:language']) == list and len(x['properties']['ucldc_schema:language']) > 0:
                while langnumb < len(x['properties']['ucldc_schema:language']):
                    numb = langnumb + 1
                    try:
                        name = "Language %d" % numb
                        if x['properties']['ucldc_schema:language'][langnumb]['language'] != None and x['properties']['ucldc_schema:language'][langnumb]['language'] != '':
                            data2[name] = x['properties']['ucldc_schema:language'][langnumb]['language']
                    except:
                        pass
                    try:
                        name = "Language %d Code" % numb
                        if x['properties']['ucldc_schema:language'][langnumb]['code'] != None and x['properties']['ucldc_schema:language'][langnumb]['code'] != '':
                            data2[name] = x['properties']['ucldc_schema:language'][langnumb]['code']
                    except:
                        pass
                    langnumb += 1
         
            tempnumb = 0
            if type(x['properties']['ucldc_schema:temporalcoverage']) == list and len(x['properties']['ucldc_schema:temporalcoverage']) > 0:
                while tempnumb < len(x['properties']['ucldc_schema:temporalcoverage']):
                    numb = tempnumb + 1
                    name = 'Temporal Coverage %d' % numb
                    data2[name]= x['properties']['ucldc_schema:temporalcoverage'][tempnumb]
                    tempnumb += 1

            if x['properties']['ucldc_schema:transcription'] != None and x['properties']['ucldc_schema:transcription'] != '':
                data2['Transcription'] = x['properties']['ucldc_schema:transcription']
            if x['properties']['ucldc_schema:accessrestrict'] != None and x['properties']['ucldc_schema:accessrestrict'] != '':
                data2['Access Restrictions'] = x['properties']['ucldc_schema:accessrestrict']
            if x['properties']['ucldc_schema:rightsstatement'] != None and x['properties']['ucldc_schema:rightsstatement'] != '':
                data2['Copyright Statement'] = x['properties']['ucldc_schema:rightsstatement']
            if x['properties']['ucldc_schema:rightsstatus'] != None and x['properties']['ucldc_schema:rightsstatus'] != '':
                data2['Copyright Status'] = x['properties']['ucldc_schema:rightsstatus']
                
            rightsnumb = 0
            if type(x['properties']['ucldc_schema:rightsholder']) == list and len(x['properties']['ucldc_schema:rightsholder']) > 0:
                while contnumb < len(x['properties']['ucldc_schema:rightsholder']):
                    numb = contnumb + 1
                    try: 
                        name = 'Copyright Holder %d Name' % numb
                        if x['properties']['ucldc_schema:rightsholder'][contnumb]['name'] != None and x['properties']['ucldc_schema:rightsholder'][contnumb]['name'] != '':
                            data2[name] = x['properties']['ucldc_schema:rightsholder'][contnumb]['name']
                    except:
                        pass
                    try: 
                        name = 'Copyright Holder %d Name Type' % numb
                        if x['properties']['ucldc_schema:rightsholder'][contnumb]['nametype'] != None and x['properties']['ucldc_schema:rightsholder'][contnumb]['nametype'] != '':
                            data2[name] = x['properties']['ucldc_schema:rightsholder'][contnumb]['nametype']
                    except:
                        pass
                    try:
                        name = 'Copyright Holder %d Source' % numb
                        if x['properties']['ucldc_schema:rightsholder'][contnumb]['source'] != None and x['properties']['ucldc_schema:rightsholder'][contnumb]['source'] != '':
                            data2[name] = x['properties']['ucldc_schema:rightsholder'][contnumb]['source']
                    except:
                        pass
                    try:
                        name = 'Copyright Holder %d Authority ID' % numb
                        if x['properties']['ucldc_schema:rightsholder'][contnumb]['authorityid'] != None and x['properties']['ucldc_schema:rightsholder'][contnumb]['authorityid'] != '':
                            data2[name] = x['properties']['ucldc_schema:rightsholder'][contnumb]['authorityid']
                    except:
                        pass
                    contnumb += 1
            
            if x['properties']['ucldc_schema:rightscontact'] != None and x['properties']['ucldc_schema:rightscontact'] != '':
                data2['Copyright Contact'] = x['properties']['ucldc_schema:rightscontact']
            if x['properties']['ucldc_schema:rightsnotice'] != None and x['properties']['ucldc_schema:rightsnotice'] != '':    
                data2['Copyright Notice'] = x['properties']['ucldc_schema:rightsnotice']
            if x['properties']['ucldc_schema:rightsdeterminationdate'] != None and x['properties']['ucldc_schema:rightsdeterminationdate'] != '':    
                data2['Copyright Determination Date'] = x['properties']['ucldc_schema:rightsdeterminationdate']
            if x['properties']['ucldc_schema:rightsstartdate'] != None and x['properties']['ucldc_schema:rightsstartdate'] != '':    
                data2['Copyright Start Date'] = x['properties']['ucldc_schema:rightsstartdate']
            if x['properties']['ucldc_schema:rightsenddate'] != None and x['properties']['ucldc_schema:rightsenddate'] != '':    
                data2['Copyright End Date'] = x['properties']['ucldc_schema:rightsenddate']
            if x['properties']['ucldc_schema:rightsjurisdiction'] != None and x['properties']['ucldc_schema:rightsjurisdiction'] != '':    
                data2['Copyright Jurisdiction'] = x['properties']['ucldc_schema:rightsjurisdiction']
            if x['properties']['ucldc_schema:rightsnote'] != None and x['properties']['ucldc_schema:rightsnote'] != '':    
                data2['Copyright Note'] = x['properties']['ucldc_schema:rightsnote']
                
            collnumb = 0
            if type(x['properties']['ucldc_schema:collection']) == list and len(x['properties']['ucldc_schema:collection']) > 0:
                while collnumb < len(x['properties']['ucldc_schema:collection']):
                    numb = collnumb + 1
                    name = 'Collection %d' % numb
                    data2[name]= x['properties']['ucldc_schema:collection'][collnumb]
                    collnumb += 1
            
            relnumb = 0
            if type(x['properties']['ucldc_schema:relatedresource']) == list and len(x['properties']['ucldc_schema:relatedresource']) > 0:
                while relnumb < len(x['properties']['ucldc_schema:relatedresource']):
                    numb = relnumb + 1
                    name = 'Related Resource %d' % numb
                    data2[name]= x['properties']['ucldc_schema:relatedresource'][relnumb]
                    relnumb += 1
           
            if x['properties']['ucldc_schema:source'] != None and x['properties']['ucldc_schema:source'] != '':
                data2['Source'] = x['properties']['ucldc_schema:source']
                
            subnumb = 0
            if type(x['properties']['ucldc_schema:subjectname']) == list and len(x['properties']['ucldc_schema:subjectname']) > 0:
                while subnumb < len(x['properties']['ucldc_schema:subjectname']):
                    numb = subnumb + 1
                    try: 
                        name = 'Subject (Name) %d Name' % numb
                        if x['properties']['ucldc_schema:subjectname'][subnumb]['name'] != None and x['properties']['ucldc_schema:subjectname'][subnumb]['name'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['name']
                    except:
                        pass
                    try: 
                        name = 'Subject (Name) %d Name Type' % numb
                        if x['properties']['ucldc_schema:subjectname'][subnumb]['name_type'] != None and x['properties']['ucldc_schema:subjectname'][subnumb]['name_type'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['name_type']
                    except:
                        pass
                    try:
                        name = 'Subject (Name) %d Role' % numb
                        if x['properties']['ucldc_schema:subjectname'][subnumb]['role'] != None and x['properties']['ucldc_schema:subjectname'][subnumb]['role'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['role']
                    except:
                        pass
                    try:
                        name = 'Subject (Name) %d Source' % numb
                        if x['properties']['ucldc_schema:subjectname'][subnumb]['source'] != None and x['properties']['ucldc_schema:subjectname'][subnumb]['source'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['source']
                    except:
                        pass
                    try:
                        name = 'Subject (Name) %d Authority ID' % numb
                        if x['properties']['ucldc_schema:subjectname'][subnumb]['authorityid'] != None and x['properties']['ucldc_schema:subjectname'][subnumb]['authorityid'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['authorityid']
                    except:
                        pass
                    subnumb += 1
           
            plcnumb = 0
            if type(x['properties']['ucldc_schema:place']) == list and len(x['properties']['ucldc_schema:place']) > 0:
                while plcnumb < len(x['properties']['ucldc_schema:place']):
                    numb = plcnumb + 1
                    try: 
                        name = 'Place %d Name' % numb
                        if x['properties']['ucldc_schema:place'][plcnumb]['name'] != None and x['properties']['ucldc_schema:place'][plcnumb]['name'] != '':
                            data2[name] = x['properties']['ucldc_schema:place'][plcnumb]['name']
                    except:
                        pass
                    try:
                        name = 'Place %d Coordinates' % numb
                        if x['properties']['ucldc_schema:place'][plcnumb]['coordinates'] != None and x['properties']['ucldc_schema:place'][plcnumb]['coordinates'] != '':
                            data2[name] = x['properties']['ucldc_schema:place'][plcnumb]['coordinates']
                    except:
                        pass
                    try:
                        name = 'Place %d Source' % numb
                        if x['properties']['ucldc_schema:place'][plcnumb]['source'] != None and x['properties']['ucldc_schema:place'][plcnumb]['source'] != '':
                            data2[name] = x['properties']['ucldc_schema:place'][plcnumb]['source']
                    except:
                        pass
                    try:
                        name = 'Place %d Authority ID' % numb
                        if x['properties']['ucldc_schema:place'][plcnumb]['authorityid'] != None and x['properties']['ucldc_schema:place'][plcnumb]['authorityid'] != '':
                            data2[name] = x['properties']['ucldc_schema:place'][plcnumb]['authorityid']
                    except:
                        pass
                    plcnumb += 1
            
            topnumb = 0
            if type(x['properties']['ucldc_schema:subjecttopic']) == list and len(x['properties']['ucldc_schema:subjecttopic']) > 0:
                while topnumb < len(x['properties']['ucldc_schema:subjecttopic']):
                    numb = topnumb + 1
                    try: 
                        name = 'Subject (Topic) %d Heading' % numb
                        if x['properties']['ucldc_schema:subjecttopic'][topnumb]['heading'] != None and x['properties']['ucldc_schema:subjecttopic'][topnumb]['heading'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjecttopic'][topnumb]['heading']
                    except:
                        pass         
                    try:
                        name = 'Subject (Topic) %d Heading Type' % numb
                        if x['properties']['ucldc_schema:subjecttopic'][topnumb]['headingtype'] != None and x['properties']['ucldc_schema:subjecttopic'][topnumb]['headingtype'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjecttopic'][topnumb]['headingtype']
                    except:
                        pass
                    try:
                        name = 'Subject (Topic) %d Source' % numb
                        if x['properties']['ucldc_schema:subjecttopic'][topnumb]['source'] != None and x['properties']['ucldc_schema:subjecttopic'][topnumb]['source'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjecttopic'][topnumb]['source']
                    except:
                        pass
                    try:
                        name = 'Subject (Topic) %d Authority ID' % numb
                        if x['properties']['ucldc_schema:subjecttopic'][topnumb]['authorityid'] != None and x['properties']['ucldc_schema:subjecttopic'][topnumb]['authorityid'] != '':
                            data2[name] = x['properties']['ucldc_schema:subjecttopic'][topnumb]['authorityid']
                    except:
                        pass
                    topnumb += 1
           
            formnumb = 0
            if type(x['properties']['ucldc_schema:formgenre']) == list and len(x['properties']['ucldc_schema:formgenre']) > 0:
                while formnumb < len(x['properties']['ucldc_schema:formgenre']):
                    numb = formnumb + 1
                    try: 
                        name = 'Form/Genre %d Heading' % numb
                        if x['properties']['ucldc_schema:formgenre'][formnumb]['heading'] != None and x['properties']['ucldc_schema:formgenre'][formnumb]['heading'] != '':
                            data2[name] = x['properties']['ucldc_schema:formgenre'][formnumb]['heading']
                    except:
                        pass           
                    try:
                        name = 'Form/Genre %d Source' % numb
                        if x['properties']['ucldc_schema:formgenre'][formnumb]['source'] != None and x['properties']['ucldc_schema:formgenre'][formnumb]['source'] != '':
                            data2[name] = x['properties']['ucldc_schema:formgenre'][formnumb]['source']
                    except:
                        pass
                    try:
                        name = 'Form/Genre %d Authority ID' % numb
                        if x['properties']['ucldc_schema:formgenre'][formnumb]['authorityid'] != None and x['properties']['ucldc_schema:formgenre'][formnumb]['authorityid'] != '':
                            data2[name] = x['properties']['ucldc_schema:formgenre'][formnumb]['authorityid']
                    except:
                        pass
                    formnumb += 1
           
            provnumb = 0
            if type(x['properties']['ucldc_schema:provenance']) == list and len(x['properties']['ucldc_schema:provenance']) > 0:
                while provnumb < len(x['properties']['ucldc_schema:provenance']):
                    numb = provnumb + 1
                    name = 'Provenance %d' % numb
                    data2[name]= x['properties']['ucldc_schema:provenance'][provnumb]
                    provnumb += 1
            
            if x['properties']['ucldc_schema:physlocation'] != None and x['properties']['ucldc_schema:physlocation'] != '':
                data2['Physical Location'] = x['properties']['ucldc_schema:physlocation']
            data.append(data2)
    fieldnames = []
    for data2 in data:
        for key, value in data2.items():
            fieldnames.append(key)
    fieldnames = list(set(fieldnames))
    fieldnames = sorted(fieldnames, reverse=True)
    return {'fieldnames':fieldnames, 'data':data, 'filename':"nuxeo_item_%s.tsv"%nx.get_metadata(path=filepath)['properties']['dc:title']}

            
def google_object(filepath, url):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    obj = object_level(filepath)
    nx = utils.Nuxeo()
    scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    with open("temp.csv", "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=obj['fieldnames'])
        writer.writeheader()
        for row in obj['data']:
            writer.writerow(row) 
    with open("temp.csv", encoding="utf8") as f:
        s = f.read() + '\n' 
    sheet_id = client.open_by_url(url).id
    client.import_csv(sheet_id, s)
    client.open_by_key(sheet_id).sheet1.update_title("nuxeo_object_%s"%nx.get_metadata(path=filepath)['properties']['dc:title'])
    os.remove("temp.csv")
    
def google_item(filepath, url):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    item = item_level(filepath)
    nx = utils.Nuxeo()
    scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    with open("temp.csv", "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=item['fieldnames'])
        writer.writeheader()
        for row in item['data']:
            writer.writerow(row) 
    with open("temp.csv", encoding="utf8") as f:
        s = f.read() + '\n' 
    sheet_id = client.open_by_url(url).id
    client.import_csv(sheet_id, s)
    client.open_by_key(sheet_id).sheet1.update_title("nuxeo_item_%s"%nx.get_metadata(path=filepath)['properties']['dc:title'])
    os.remove("temp.csv")

if 'O' in choice or 'o' in choice:
    if 'http' in url:
        try:
            google_object(filepath, url)
        except:
            print("\n*********\nWriting to Google document did not work. Make sure that Google document has been shared with API key email address")
    else:
        obj = object_level(filepath)
        with open(obj['filename'], "wb") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=obj['fieldnames'], delimiter="\t")
            writer.writeheader()
            for row in obj['data']:
                writer.writerow(row) 
if 'I' in choice or 'i' in choice:
    if 'http' in url:
        try:
            google_item(filepath, url)
        except:
            print("\n*********\nWriting to Google document did not work. Make sure that Google document has been shared with API key email address")
    else:  
        item = item_level(filepath)
        with open(item['filename'], "wb") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=item['fieldnames'], delimiter="\t")
            writer.writeheader()
            for row in item['data']:
                writer.writerow(row) 
    
