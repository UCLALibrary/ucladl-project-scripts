import unicodecsv as csv
import os 
filepath = input('Enter Nuxeo File Path: ') 
choice = input('Object Level (ENTER O) or Item Level (ENTER I): ')
url = input('Enter Google Sheet URL: ')
from pynux import utils

def object_level(filepath):
    nx = utils.Nuxeo()
    data = []
    for n in nx.children(filepath):
        data2 = {}
        data2['File path'] = n['path']
        data2['Title'] = n['properties']['dc:title']
        data2['Type'] = n['properties']['ucldc_schema:type']
        altnumb = 0
        if type(n['properties']['ucldc_schema:alternativetitle']) == list and len(n['properties']['ucldc_schema:alternativetitle']) > 0:
            while altnumb < len(n['properties']['ucldc_schema:alternativetitle']):
                numb = altnumb + 1
                name = 'Alternative Title %d' % numb
                data2[name]= n['properties']['ucldc_schema:alternativetitle'][altnumb]
                altnumb += 1
        else:
            data2['Alternative Title 1']= ''
        data2['Identifier'] = n['properties']['ucldc_schema:identifier']
        locnumb = 0
        if type(n['properties']['ucldc_schema:localidentifier']) == list and len(n['properties']['ucldc_schema:localidentifier']) > 0:
            while locnumb < len(n['properties']['ucldc_schema:localidentifier']):
                numb = locnumb + 1
                name = 'Local Identifier %d' % numb
                data2[name]= n['properties']['ucldc_schema:localidentifier'][locnumb]
                locnumb += 1
        else:
            data2['Local Identifier 1'] = ''
        campnumb = 0
        if type(n['properties']['ucldc_schema:campusunit']) == list and len(n['properties']['ucldc_schema:campusunit']) > 0:
            while campnumb < len(n['properties']['ucldc_schema:campusunit']):
                numb = campnumb + 1
                name = 'Campus/Unit %d' % numb
                data2[name]= n['properties']['ucldc_schema:campusunit'][campnumb]
                campnumb += 1
        else:
            data2['Campus/Unit 1'] = ''
        datenumb = 0
        if type(n['properties']['ucldc_schema:date']) == list and len(n['properties']['ucldc_schema:date']) > 0:
            while datenumb < len(n['properties']['ucldc_schema:date']):
                numb = datenumb + 1
                try: 
                    name = 'Date %d' % numb
                    data2[name] = n['properties']['ucldc_schema:date'][datenumb]['date']
                except:
                    data2['Date 1'] = ''
                try: 
                    name = 'Date %d Type' % numb
                    data2[name] = n['properties']['ucldc_schema:date'][datenumb]['datetype']
                except:
                    data2['Date 1 Type'] = ''
                try:
                    name = 'Date %d Inclusive Start' % numb
                    data2[name] = n['properties']['ucldc_schema:date'][datenumb]['inclusivestart']
                except:
                    data2['Date 1 Inclusive Start'] = ''
                try:
                    name = 'Date %d Inclusive End' % numb
                    data2[name] = n['properties']['ucldc_schema:date'][datenumb]['inclusiveend']
                except:
                    data2['Date 1 Inclusive End'] = ''
                try:
                    name = 'Date %d Single' % numb
                    data2[name] = n['properties']['ucldc_schema:date'][datenumb]['single']
                except:
                    data2['Date 1 Single'] = ''
                datenumb += 1
        else:
            data2['Date 1'] = ''
            data2['Date 1 Type'] = ''
            data2['Date 1 Inclusive Start'] = ''
            data2['Date 1 Inclusive End'] = ''
            data2['Date 1 Single'] = ''
        pubnumb = 0
        if type(n['properties']['ucldc_schema:publisher']) == list and len(n['properties']['ucldc_schema:publisher']) > 0:
            while pubnumb < len(n['properties']['ucldc_schema:publisher']):
                numb = pubnumb + 1
                name = 'Publication/Origination Info %d' % numb
                data2[name]= n['properties']['ucldc_schema:publisher'][pubnumb]
                pubnumb += 1
        else:
            data2['Publication/Origination Info 1'] = ''
        creatnumb = 0
        if type(n['properties']['ucldc_schema:creator']) == list and len(n['properties']['ucldc_schema:creator']) > 0:
            while creatnumb < len(n['properties']['ucldc_schema:creator']):
                numb = creatnumb + 1
                try: 
                    name = 'Creator %d Name' % numb
                    data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['name']
                except:
                    data2['Creator 1 Name'] = ''
                try: 
                    name = 'Creator %d Name Type' % numb
                    data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['nametype']
                except:
                    data2['Creator 1 Name Type'] = ''
                try:
                    name = 'Creator %d Role' % numb
                    data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['role']
                except:
                    data2['Creator 1 Role'] = ''
                try:
                    name = 'Creator %d Source' % numb
                    data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['source']
                except:
                    data2['Creator 1 Source'] = ''
                try:
                    name = 'Creator %d Authority ID' % numb
                    data2[name] = n['properties']['ucldc_schema:creator'][creatnumb]['authorityid']
                except:
                    data2['Creator 1 Authority ID'] = ''
                creatnumb += 1
        else:
            data2['Creator 1 Name'] = ''
            data2['Creator 1 Name Type'] = ''
            data2['Creator 1 Role'] = ''
            data2['Creator 1 Source'] = ''
            data2['Creator 1 Authority ID'] = ''
        contnumb = 0
        if type(n['properties']['ucldc_schema:contributor']) == list and len(n['properties']['ucldc_schema:contributor']) > 0:
            while contnumb < len(n['properties']['ucldc_schema:contributor']):
                numb = contnumb + 1
                try: 
                    name = 'Contributor %d Name' % numb
                    data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['name']
                except:
                    data2['Contributor 1 Name'] = ''
                try: 
                    name = 'Contributor %d Name Type' % numb
                    data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['nametype']
                except:
                    data2['Contributor 1 Name Type'] = ''
                try:
                    name = 'Contributor %d Role' % numb
                    data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['role']
                except:
                    data2['Contributor 1 Role'] = ''
                try:
                    name = 'Contributor %d Source' % numb
                    data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['source']
                except:
                    data2['Contributor 1 Source'] = ''
                try:
                    name = 'Contributor %d Authority ID' % numb
                    data2[name] = n['properties']['ucldc_schema:contributor'][contnumb]['authorityid']
                except:
                    data2['Contributor 1 Authority ID'] = ''
                contnumb += 1
        else:
            data2['Contributor 1 Name'] = ''
            data2['Contributor 1 Name Type'] = ''
            data2['Contributor 1 Role'] = ''
            data2['Contributor 1 Source'] = ''
            data2['Contributor 1 Authority ID'] = ''
        data2['Format/Physical Description'] = n['properties']['ucldc_schema:physdesc']
        descnumb = 0
        if type(n['properties']['ucldc_schema:description']) == list and len(n['properties']['ucldc_schema:description']) > 0:
            while descnumb < len(n['properties']['ucldc_schema:description']):
                numb = descnumb + 1
                try:
                    name = "Description %d Note" % numb
                    data2[name] = n['properties']['ucldc_schema:description'][descnumb]['item']
                except:
                    data2['Description 1 Note'] = ''
                try:
                    name = "Description %d Type" % numb
                    data2[name] = n['properties']['ucldc_schema:description'][descnumb]['type']
                except:
                    data2['Description 1 Type'] = ''
                descnumb += 1
        else:
            data2['Description 1 Note'] = ''
            data2['Description 1 Type'] = ''
        data2['Extent'] = n['properties']['ucldc_schema:extent']
        langnumb = 0
        if type(n['properties']['ucldc_schema:language']) == list and len(n['properties']['ucldc_schema:language']) > 0:
            while langnumb < len(n['properties']['ucldc_schema:language']):
                numb = langnumb + 1
                try:
                    name = "Language %d" % numb
                    data2[name] = n['properties']['ucldc_schema:language'][langnumb]['language']
                except:
                    data2['Language 1'] = ''
                try:
                    name = "Language %d Code" % numb
                    data2[name] = n['properties']['ucldc_schema:language'][langnumb]['code']
                except:
                    data2['Language 1 Code'] = ''
                langnumb += 1
        else:
            data2['Language 1'] = ''
            data2['Language 1 Code'] = ''
        tempnumb = 0
        if type(n['properties']['ucldc_schema:temporalcoverage']) == list and len(n['properties']['ucldc_schema:temporalcoverage']) > 0:
            while tempnumb < len(n['properties']['ucldc_schema:temporalcoverage']):
                numb = tempnumb + 1
                name = 'Temporal Coverage %d' % numb
                data2[name]= n['properties']['ucldc_schema:temporalcoverage'][tempnumb]
                tempnumb += 1
        else:
            data2['Temporal Coverage 1'] = ''
        data2['Transcription'] = n['properties']['ucldc_schema:transcription']
        data2['Access Restrictions'] = n['properties']['ucldc_schema:accessrestrict']
        data2['Copyright Statement'] = n['properties']['ucldc_schema:rightsstatement']
        data2['Copyright Status'] = n['properties']['ucldc_schema:rightsstatus']
        rightsnumb = 0
        if type(n['properties']['ucldc_schema:rightsholder']) == list and len(n['properties']['ucldc_schema:rightsholder']) > 0:
            while contnumb < len(n['properties']['ucldc_schema:rightsholder']):
                numb = contnumb + 1
                try: 
                    name = 'Copyright Holder %d Name' % numb
                    data2[name] = n['properties']['ucldc_schema:rightsholder'][contnumb]['name']
                except:
                    data2['Copyright Holder 1 Name'] = ''
                try: 
                    name = 'Copyright Holder %d Name Type' % numb
                    data2[name] = n['properties']['ucldc_schema:rightsholder'][contnumb]['nametype']
                except:
                    data2['Copyright Holder 1 Name Type'] = ''
                try:
                    name = 'Copyright Holder %d Source' % numb
                    data2[name] = n['properties']['ucldc_schema:rightsholder'][contnumb]['source']
                except:
                    data2['Copyright Holder 1 Source'] = ''
                try:
                    name = 'Copyright Holder %d Authority ID' % numb
                    data2[name] = n['properties']['ucldc_schema:rightsholder'][contnumb]['authorityid']
                except:
                    data2['Copyright Holder 1 Authority ID'] = ''
                contnumb += 1
        else:
            data2['Copyright Holder 1 Name'] = ''
            data2['Copyright Holder 1 Name Type'] = ''
            data2['Copyright Holder 1 Source'] = ''
            data2['Copyright Holder 1 Authority ID'] = ''
        data2['Copyright Contact'] = n['properties']['ucldc_schema:rightscontact']
        data2['Copyright Notice'] = n['properties']['ucldc_schema:rightsnotice']
        data2['Copyright Determination Date'] = n['properties']['ucldc_schema:rightsdeterminationdate']
        data2['Copyright Start Date'] = n['properties']['ucldc_schema:rightsstartdate']
        data2['Copyright End Date'] = n['properties']['ucldc_schema:rightsenddate']
        data2['Copyright Jurisdiction'] = n['properties']['ucldc_schema:rightsjurisdiction']
        data2['Copyright Note'] = n['properties']['ucldc_schema:rightsnote']
        collnumb = 0
        if type(n['properties']['ucldc_schema:collection']) == list and len(n['properties']['ucldc_schema:collection']) > 0:
            while collnumb < len(n['properties']['ucldc_schema:collection']):
                numb = collnumb + 1
                name = 'Collection %d' % numb
                data2[name]= n['properties']['ucldc_schema:collection'][collnumb]
                collnumb += 1
        else:
            data2['Collection 1'] = ''
        relnumb = 0
        if type(n['properties']['ucldc_schema:relatedresource']) == list and len(n['properties']['ucldc_schema:relatedresource']) > 0:
            while relnumb < len(n['properties']['ucldc_schema:relatedresource']):
                numb = relnumb + 1
                name = 'Related Resource %d' % numb
                data2[name]= n['properties']['ucldc_schema:relatedresource'][relnumb]
                relnumb += 1
        else:
            data2['Related Resource 1'] = ''
        data2['Source'] = n['properties']['ucldc_schema:source']
        subnumb = 0
        if type(n['properties']['ucldc_schema:subjectname']) == list and len(n['properties']['ucldc_schema:subjectname']) > 0:
            while subnumb < len(n['properties']['ucldc_schema:subjectname']):
                numb = subnumb + 1
                try: 
                    name = 'Subject (Name) %d Name' % numb
                    data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['name']
                except:
                    data2['Subject (Name) 1 Name'] = ''
                try: 
                    name = 'Subject (Name) %d Name Type' % numb
                    data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['name_type']
                except:
                    data2['Subject (Name) 1 Name Type'] = ''
                try:
                    name = 'Subject (Name) %d Role' % numb
                    data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['role']
                except:
                    data2['Subject (Name) 1 Role'] = ''
                try:
                    name = 'Subject (Name) %d Source' % numb
                    data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['source']
                except:
                    data2['Subject (Name) 1 Source'] = ''
                try:
                    name = 'Subject (Name) %d Authority ID' % numb
                    data2[name] = n['properties']['ucldc_schema:subjectname'][subnumb]['authorityid']
                except:
                    data2['Subject (Name) 1 Authority ID'] = ''
                subnumb += 1
        else:
            data2['Subject (Name) 1 Name'] = ''
            data2['Subject (Name) 1 Name Type'] = ''
            data2['Subject (Name) 1 Role'] = ''
            data2['Subject (Name) 1 Source'] = ''
            data2['Subject (Name) 1 Authority ID'] = ''
        plcnumb = 0
        if type(n['properties']['ucldc_schema:place']) == list and len(n['properties']['ucldc_schema:place']) > 0:
            while plcnumb < len(n['properties']['ucldc_schema:place']):
                numb = plcnumb + 1
                try: 
                    name = 'Place %d Name' % numb
                    data2[name] = n['properties']['ucldc_schema:place'][plcnumb]['name']
                except:
                    data2['Place 1 Name'] = ''
                try:
                    name = 'Place %d Coordinates' % numb
                    data2[name] = n['properties']['ucldc_schema:place'][plcnumb]['coordinates']
                except:
                    data2['Place 1 Coordinates'] = ''
                try:
                    name = 'Place %d Source' % numb
                    data2[name] = n['properties']['ucldc_schema:place'][plcnumb]['source']
                except:
                    data2['Place 1 Source'] = ''
                try:
                    name = 'Place %d Authority ID' % numb
                    data2[name] = n['properties']['ucldc_schema:place'][plcnumb]['authorityid']
                except:
                    data2['Place 1 Authority ID'] = ''
                plcnumb += 1
        else:
            data2['Place 1 Name'] = ''
            data2['Place 1 Coordinates'] = ''
            data2['Place 1 Source'] = ''
            data2['Place 1 Authority ID'] = ''
        topnumb = 0
        if type(n['properties']['ucldc_schema:subjecttopic']) == list and len(n['properties']['ucldc_schema:subjecttopic']) > 0:
            while topnumb < len(n['properties']['ucldc_schema:subjecttopic']):
                numb = topnumb + 1
                try: 
                    name = 'Subject (Topic) %d Heading' % numb
                    data2[name] = n['properties']['ucldc_schema:subjecttopic'][topnumb]['heading']
                except:
                    data2['Subject (Topic) 1 Heading'] = ''			
                try:
                    name = 'Subject (Topic) %d Heading Type' % numb
                    data2[name] = n['properties']['ucldc_schema:subjecttopic'][topnumb]['headingtype']
                except:
                    data2['Subject (Topic) 1 Heading Type'] = ''
                try:
                    name = 'Subject (Topic) %d Source' % numb
                    data2[name] = n['properties']['ucldc_schema:subjecttopic'][topnumb]['source']
                except:
                    data2['Subject (Topic) 1 Source'] = ''
                try:
                    name = 'Subject (Topic) %d Authority ID' % numb
                    data2[name] = n['properties']['ucldc_schema:subjecttopic'][topnumb]['authorityid']
                except:
                    data2['Subject (Topic) 1 Authority ID'] = ''
                topnumb += 1
        else:
            data2['Subject (Topic) 1 Heading'] = ''	
            data2['Subject (Topic) 1 Heading Type'] = ''
            data2['Subject (Topic) 1 Source'] = ''
            data2['Subject (Topic) 1 Authority ID'] = ''
        formnumb = 0
        if type(n['properties']['ucldc_schema:formgenre']) == list and len(n['properties']['ucldc_schema:formgenre']) > 0:
            while formnumb < len(n['properties']['ucldc_schema:formgenre']):
                numb = formnumb + 1
                try: 
                    name = 'Form/Genre %d Heading' % numb
                    data2[name] = n['properties']['ucldc_schema:formgenre'][formnumb]['heading']
                except:
                    data2['Form/Genre 1 Heading'] = ''			
                try:
                    name = 'Form/Genre %d Source' % numb
                    data2[name] = n['properties']['ucldc_schema:formgenre'][formnumb]['source']
                except:
                    data2['Form/Genre 1 Source'] = ''
                try:
                    name = 'Form/Genre %d Authority ID' % numb
                    data2[name] = n['properties']['ucldc_schema:formgenre'][formnumb]['authorityid']
                except:
                    data2['Form/Genre 1 Authority ID'] = ''
                formnumb += 1
        else:
            data2['Form/Genre 1 Heading'] = ''	
            data2['Form/Genre 1 Source'] = ''
            data2['Form/Genre 1 Authority ID'] = ''
        provnumb = 0
        if type(n['properties']['ucldc_schema:provenance']) == list and len(n['properties']['ucldc_schema:provenance']) > 0:
            while provnumb < len(n['properties']['ucldc_schema:provenance']):
                numb = provnumb + 1
                name = 'Provenance %d' % numb
                data2[name]= n['properties']['ucldc_schema:provenance'][provnumb]
                provnumb += 1
        else:
            data2['Provenance 1'] = ''
        data2['Physical Location'] = n['properties']['ucldc_schema:physlocation']
        data.append(data2)
    #print(data)
    fieldnames = []
    for data2 in data:
        for key, value in data2.items():
            fieldnames.append(key)
    fieldnames = list(set(fieldnames))
    fieldnames = sorted(fieldnames, reverse=True)
    with open("nuxeo_object_%s.tsv"%nx.get_metadata(path=filepath)['properties']['dc:title'], "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return {'fieldnames':fieldnames, 'data':data}
    
    
def item_level(filepath):
    nx = utils.Nuxeo()
    data = []
    for n in nx.children(filepath):
        for x in nx.children(n['path']):
            data2 = {}
            data2['File path'] = x['path']
            data2['Title'] = x['properties']['dc:title']
            data2['Type'] = x['properties']['ucldc_schema:type']
            altnumb = 0
            if type(x['properties']['ucldc_schema:alternativetitle']) == list and len(x['properties']['ucldc_schema:alternativetitle']) > 0:
                while altnumb < len(x['properties']['ucldc_schema:alternativetitle']):
                    numb = altnumb + 1
                    name = 'Alternative Title %d' % numb
                    data2[name]= x['properties']['ucldc_schema:alternativetitle'][altnumb]
                    altnumb += 1
            else:
                data2['Alternative Title 1']= ''
            data2['Identifier'] = x['properties']['ucldc_schema:identifier']
            locnumb = 0
            if type(x['properties']['ucldc_schema:localidentifier']) == list and len(x['properties']['ucldc_schema:localidentifier']) > 0:
                while locnumb < len(x['properties']['ucldc_schema:localidentifier']):
                    numb = locnumb + 1
                    name = 'Local Identifier %d' % numb
                    data2[name]= x['properties']['ucldc_schema:localidentifier'][locnumb]
                    locnumb += 1
            else:
                data2['Local Identifier 1'] = ''
            campnumb = 0
            if type(x['properties']['ucldc_schema:campusunit']) == list and len(x['properties']['ucldc_schema:campusunit']) > 0:
                while campnumb < len(x['properties']['ucldc_schema:campusunit']):
                    numb = campnumb + 1
                    name = 'Campus/Unit %d' % numb
                    data2[name]= x['properties']['ucldc_schema:campusunit'][campnumb]
                    campnumb += 1
            else:
                data2['Campus/Unit 1'] = ''
            datenumb = 0
            if type(x['properties']['ucldc_schema:date']) == list and len(x['properties']['ucldc_schema:date']) > 0:
                while datenumb < len(x['properties']['ucldc_schema:date']):
                    numb = datenumb + 1
                    try: 
                        name = 'Date %d' % numb
                        data2[name] = x['properties']['ucldc_schema:date'][datenumb]['date']
                    except:
                        data2['Date 1'] = ''
                    try: 
                        name = 'Date %d Type' % numb
                        data2[name] = x['properties']['ucldc_schema:date'][datenumb]['datetype']
                    except:
                        data2['Date 1 Type'] = ''
                    try:
                        name = 'Date %d Inclusive Start' % numb
                        data2[name] = x['properties']['ucldc_schema:date'][datenumb]['inclusivestart']
                    except:
                        data2['Date 1 Inclusive Start'] = ''
                    try:
                        name = 'Date %d Inclusive End' % numb
                        data2[name] = x['properties']['ucldc_schema:date'][datenumb]['inclusiveend']
                    except:
                        data2['Date 1 Inclusive End'] = ''
                    try:
                        name = 'Date %d Single' % numb
                        data2[name] = x['properties']['ucldc_schema:date'][datenumb]['single']
                    except:
                        data2['Date 1 Single'] = ''
                    datenumb += 1
            else:
                data2['Date 1'] = ''
                data2['Date 1 Type'] = ''
                data2['Date 1 Inclusive Start'] = ''
                data2['Date 1 Inclusive End'] = ''
                data2['Date 1 Single'] = ''
            pubnumb = 0
            if type(x['properties']['ucldc_schema:publisher']) == list and len(x['properties']['ucldc_schema:publisher']) > 0:
                while pubnumb < len(x['properties']['ucldc_schema:publisher']):
                    numb = pubnumb + 1
                    name = 'Publication/Origination Info %d' % numb
                    data2[name]= x['properties']['ucldc_schema:publisher'][pubnumb]
                    pubnumb += 1
            else:
                data2['Publication/Origination Info 1'] = ''
            creatnumb = 0
            if type(x['properties']['ucldc_schema:creator']) == list and len(x['properties']['ucldc_schema:creator']) > 0:
                while creatnumb < len(x['properties']['ucldc_schema:creator']):
                    numb = creatnumb + 1
                    try: 
                        name = 'Creator %d Name' % numb
                        data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['name']
                    except:
                        data2['Creator 1 Name'] = ''
                    try: 
                        name = 'Creator %d Name Type' % numb
                        data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['nametype']
                    except:
                        data2['Creator 1 Name Type'] = ''
                    try:
                        name = 'Creator %d Role' % numb
                        data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['role']
                    except:
                        data2['Creator 1 Role'] = ''
                    try:
                        name = 'Creator %d Source' % numb
                        data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['source']
                    except:
                        data2['Creator 1 Source'] = ''
                    try:
                        name = 'Creator %d Authority ID' % numb
                        data2[name] = x['properties']['ucldc_schema:creator'][creatnumb]['authorityid']
                    except:
                        data2['Creator 1 Authority ID'] = ''
                    creatnumb += 1
            else:
                data2['Creator 1 Name'] = ''
                data2['Creator 1 Name Type'] = ''
                data2['Creator 1 Role'] = ''
                data2['Creator 1 Source'] = ''
                data2['Creator 1 Authority ID'] = ''
            contnumb = 0
            if type(x['properties']['ucldc_schema:contributor']) == list and len(x['properties']['ucldc_schema:contributor']) > 0:
                while contnumb < len(x['properties']['ucldc_schema:contributor']):
                    numb = contnumb + 1
                    try: 
                        name = 'Contributor %d Name' % numb
                        data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['name']
                    except:
                        data2['Contributor 1 Name'] = ''
                    try: 
                        name = 'Contributor %d Name Type' % numb
                        data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['nametype']
                    except:
                        data2['Contributor 1 Name Type'] = ''
                    try:
                        name = 'Contributor %d Role' % numb
                        data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['role']
                    except:
                        data2['Contributor 1 Role'] = ''
                    try:
                        name = 'Contributor %d Source' % numb
                        data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['source']
                    except:
                        data2['Contributor 1 Source'] = ''
                    try:
                        name = 'Contributor %d Authority ID' % numb
                        data2[name] = x['properties']['ucldc_schema:contributor'][contnumb]['authorityid']
                    except:
                        data2['Contributor 1 Authority ID'] = ''
                    contnumb += 1
            else:
                data2['Contributor 1 Name'] = ''
                data2['Contributor 1 Name Type'] = ''
                data2['Contributor 1 Role'] = ''
                data2['Contributor 1 Source'] = ''
                data2['Contributor 1 Authority ID'] = ''
            data2['Format/Physical Description'] = x['properties']['ucldc_schema:physdesc']
            descnumb = 0
            if type(x['properties']['ucldc_schema:description']) == list and len(x['properties']['ucldc_schema:description']) > 0:
                while descnumb < len(x['properties']['ucldc_schema:description']):
                    numb = descnumb + 1
                    try:
                        name = "Description %d Note" % numb
                        data2[name] = x['properties']['ucldc_schema:description'][descnumb]['item']
                    except:
                        data2['Description 1 Note'] = ''
                    try:
                        name = "Description %d Type" % numb
                        data2[name] = x['properties']['ucldc_schema:description'][descnumb]['type']
                    except:
                        data2['Description 1 Type'] = ''
                    descnumb += 1
            else:
                data2['Description 1 Note'] = ''
                data2['Description 1 Type'] = ''
            data2['Extent'] = x['properties']['ucldc_schema:extent']
            langnumb = 0
            if type(x['properties']['ucldc_schema:language']) == list and len(x['properties']['ucldc_schema:language']) > 0:
                while langnumb < len(x['properties']['ucldc_schema:language']):
                    numb = langnumb + 1
                    try:
                        name = "Language %d" % numb
                        data2[name] = x['properties']['ucldc_schema:language'][langnumb]['language']
                    except:
                        data2['Language 1'] = ''
                    try:
                        name = "Language %d Code" % numb
                        data2[name] = x['properties']['ucldc_schema:language'][langnumb]['code']
                    except:
                        data2['Language 1 Code'] = ''
                    langnumb += 1
            else:
                data2['Language 1'] = ''
                data2['Language 1 Code'] = ''
            tempnumb = 0
            if type(x['properties']['ucldc_schema:temporalcoverage']) == list and len(x['properties']['ucldc_schema:temporalcoverage']) > 0:
                while tempnumb < len(x['properties']['ucldc_schema:temporalcoverage']):
                    numb = tempnumb + 1
                    name = 'Temporal Coverage %d' % numb
                    data2[name]= x['properties']['ucldc_schema:temporalcoverage'][tempnumb]
                    tempnumb += 1
            else:
                data2['Temporal Coverage 1'] = ''
            data2['Transcription'] = x['properties']['ucldc_schema:transcription']
            data2['Access Restrictions'] = x['properties']['ucldc_schema:accessrestrict']
            data2['Copyright Statement'] = x['properties']['ucldc_schema:rightsstatement']
            data2['Copyright Status'] = x['properties']['ucldc_schema:rightsstatus']
            rightsnumb = 0
            if type(x['properties']['ucldc_schema:rightsholder']) == list and len(x['properties']['ucldc_schema:rightsholder']) > 0:
                while contnumb < len(x['properties']['ucldc_schema:rightsholder']):
                    numb = contnumb + 1
                    try: 
                        name = 'Copyright Holder %d Name' % numb
                        data2[name] = x['properties']['ucldc_schema:rightsholder'][contnumb]['name']
                    except:
                        data2['Copyright Holder 1 Name'] = ''
                    try: 
                        name = 'Copyright Holder %d Name Type' % numb
                        data2[name] = x['properties']['ucldc_schema:rightsholder'][contnumb]['nametype']
                    except:
                        data2['Copyright Holder 1 Name Type'] = ''
                    try:
                        name = 'Copyright Holder %d Source' % numb
                        data2[name] = x['properties']['ucldc_schema:rightsholder'][contnumb]['source']
                    except:
                        data2['Copyright Holder 1 Source'] = ''
                    try:
                        name = 'Copyright Holder %d Authority ID' % numb
                        data2[name] = x['properties']['ucldc_schema:rightsholder'][contnumb]['authorityid']
                    except:
                        data2['Copyright Holder 1 Authority ID'] = ''
                    contnumb += 1
            else:
                data2['Copyright Holder 1 Name'] = ''
                data2['Copyright Holder 1 Name Type'] = ''
                data2['Copyright Holder 1 Source'] = ''
                data2['Copyright Holder 1 Authority ID'] = ''
            data2['Copyright Contact'] = x['properties']['ucldc_schema:rightscontact']
            data2['Copyright Notice'] = x['properties']['ucldc_schema:rightsnotice']
            data2['Copyright Determination Date'] = x['properties']['ucldc_schema:rightsdeterminationdate']
            data2['Copyright Start Date'] = x['properties']['ucldc_schema:rightsstartdate']
            data2['Copyright End Date'] = x['properties']['ucldc_schema:rightsenddate']
            data2['Copyright Jurisdiction'] = x['properties']['ucldc_schema:rightsjurisdiction']
            data2['Copyright Note'] = x['properties']['ucldc_schema:rightsnote']
            collnumb = 0
            if type(x['properties']['ucldc_schema:collection']) == list and len(x['properties']['ucldc_schema:collection']) > 0:
                while collnumb < len(x['properties']['ucldc_schema:collection']):
                    numb = collnumb + 1
                    name = 'Collection %d' % numb
                    data2[name]= x['properties']['ucldc_schema:collection'][collnumb]
                    collnumb += 1
            else:
                data2['Collection 1'] = ''
            relnumb = 0
            if type(x['properties']['ucldc_schema:relatedresource']) == list and len(x['properties']['ucldc_schema:relatedresource']) > 0:
                while relnumb < len(x['properties']['ucldc_schema:relatedresource']):
                    numb = relnumb + 1
                    name = 'Related Resource %d' % numb
                    data2[name]= x['properties']['ucldc_schema:relatedresource'][relnumb]
                    relnumb += 1
            else:
                data2['Related Resource 1'] = ''
            data2['Source'] = x['properties']['ucldc_schema:source']
            subnumb = 0
            if type(x['properties']['ucldc_schema:subjectname']) == list and len(x['properties']['ucldc_schema:subjectname']) > 0:
                while subnumb < len(x['properties']['ucldc_schema:subjectname']):
                    numb = subnumb + 1
                    try: 
                        name = 'Subject (Name) %d Name' % numb
                        data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['name']
                    except:
                        data2['Subject (Name) 1 Name'] = ''
                    try: 
                        name = 'Subject (Name) %d Name Type' % numb
                        data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['name_type']
                    except:
                        data2['Subject (Name) 1 Name Type'] = ''
                    try:
                        name = 'Subject (Name) %d Role' % numb
                        data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['role']
                    except:
                        data2['Subject (Name) 1 Role'] = ''
                    try:
                        name = 'Subject (Name) %d Source' % numb
                        data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['source']
                    except:
                        data2['Subject (Name) 1 Source'] = ''
                    try:
                        name = 'Subject (Name) %d Authority ID' % numb
                        data2[name] = x['properties']['ucldc_schema:subjectname'][subnumb]['authorityid']
                    except:
                        data2['Subject (Name) 1 Authority ID'] = ''
                    subnumb += 1
            else:
                data2['Subject (Name) 1 Name'] = ''
                data2['Subject (Name) 1 Name Type'] = ''
                data2['Subject (Name) 1 Role'] = ''
                data2['Subject (Name) 1 Source'] = ''
                data2['Subject (Name) 1 Authority ID'] = ''
            plcnumb = 0
            if type(x['properties']['ucldc_schema:place']) == list and len(x['properties']['ucldc_schema:place']) > 0:
                while plcnumb < len(x['properties']['ucldc_schema:place']):
                    numb = plcnumb + 1
                    try: 
                        name = 'Place %d Name' % numb
                        data2[name] = x['properties']['ucldc_schema:place'][plcnumb]['name']
                    except:
                        data2['Place 1 Name'] = ''
                    try:
                        name = 'Place %d Coordinates' % numb
                        data2[name] = x['properties']['ucldc_schema:place'][plcnumb]['coordinates']
                    except:
                        data2['Place 1 Coordinates'] = ''
                    try:
                        name = 'Place %d Source' % numb
                        data2[name] = x['properties']['ucldc_schema:place'][plcnumb]['source']
                    except:
                        data2['Place 1 Source'] = ''
                    try:
                        name = 'Place %d Authority ID' % numb
                        data2[name] = x['properties']['ucldc_schema:place'][plcnumb]['authorityid']
                    except:
                        data2['Place 1 Authority ID'] = ''
                    plcnumb += 1
            else:
                data2['Place 1 Name'] = ''
                data2['Place 1 Coordinates'] = ''
                data2['Place 1 Source'] = ''
                data2['Place 1 Authority ID'] = ''
            topnumb = 0
            if type(x['properties']['ucldc_schema:subjecttopic']) == list and len(x['properties']['ucldc_schema:subjecttopic']) > 0:
                while topnumb < len(x['properties']['ucldc_schema:subjecttopic']):
                    numb = topnumb + 1
                    try: 
                        name = 'Subject (Topic) %d Heading' % numb
                        data2[name] = x['properties']['ucldc_schema:subjecttopic'][topnumb]['heading']
                    except:
                        data2['Subject (Topic) 1 Heading'] = ''            
                    try:
                        name = 'Subject (Topic) %d Heading Type' % numb
                        data2[name] = x['properties']['ucldc_schema:subjecttopic'][topnumb]['headingtype']
                    except:
                        data2['Subject (Topic) 1 Heading Type'] = ''
                    try:
                        name = 'Subject (Topic) %d Source' % numb
                        data2[name] = x['properties']['ucldc_schema:subjecttopic'][topnumb]['source']
                    except:
                        data2['Subject (Topic) 1 Source'] = ''
                    try:
                        name = 'Subject (Topic) %d Authority ID' % numb
                        data2[name] = x['properties']['ucldc_schema:subjecttopic'][topnumb]['authorityid']
                    except:
                        data2['Subject (Topic) 1 Authority ID'] = ''
                    topnumb += 1
            else:
                data2['Subject (Topic) 1 Heading'] = ''    
                data2['Subject (Topic) 1 Heading Type'] = ''
                data2['Subject (Topic) 1 Source'] = ''
                data2['Subject (Topic) 1 Authority ID'] = ''
            formnumb = 0
            if type(x['properties']['ucldc_schema:formgenre']) == list and len(x['properties']['ucldc_schema:formgenre']) > 0:
                while formnumb < len(x['properties']['ucldc_schema:formgenre']):
                    numb = formnumb + 1
                    try: 
                        name = 'Form/Genre %d Heading' % numb
                        data2[name] = x['properties']['ucldc_schema:formgenre'][formnumb]['heading']
                    except:
                        data2['Form/Genre 1 Heading'] = ''            
                    try:
                        name = 'Form/Genre %d Source' % numb
                        data2[name] = x['properties']['ucldc_schema:formgenre'][formnumb]['source']
                    except:
                        data2['Form/Genre 1 Source'] = ''
                    try:
                        name = 'Form/Genre %d Authority ID' % numb
                        data2[name] = x['properties']['ucldc_schema:formgenre'][formnumb]['authorityid']
                    except:
                        data2['Form/Genre 1 Authority ID'] = ''
                    formnumb += 1
            else:
                data2['Form/Genre 1 Heading'] = ''    
                data2['Form/Genre 1 Source'] = ''
                data2['Form/Genre 1 Authority ID'] = ''
            provnumb = 0
            if type(x['properties']['ucldc_schema:provenance']) == list and len(x['properties']['ucldc_schema:provenance']) > 0:
                while provnumb < len(x['properties']['ucldc_schema:provenance']):
                    numb = provnumb + 1
                    name = 'Provenance %d' % numb
                    data2[name]= x['properties']['ucldc_schema:provenance'][provnumb]
                    provnumb += 1
            else:
                data2['Provenance 1'] = ''
            data2['Physical Location'] = x['properties']['ucldc_schema:physlocation']
            data.append(data2)
    fieldnames = []
    for data2 in data:
        for key, value in data2.items():
            fieldnames.append(key)
    fieldnames = list(set(fieldnames))
    fieldnames = sorted(fieldnames, reverse=True)
    with open("nuxeo_item_%s.tsv"%nx.get_metadata(path=filepath)['properties']['dc:title'], "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return {'fieldnames':fieldnames, 'data':data}
def google_object(filepath, url):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    obj = object_level(filepath)
    nx = utils.Nuxeo()
    scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    with open("nuxeo_object_%s.tsv"%nx.get_metadata(path=filepath)['properties']['dc:title'], encoding="utf8") as f:
        s = f.read().replace("\t", ",") + '\n' 
    sheet_id = client.open_by_url(url).id
    client.import_csv(sheet_id, s)
    os.remove("nuxeo_object_%s.tsv"%nx.get_metadata(path=filepath)['properties']['dc:title'])
def google_item(filepath, url):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    item = item_level(filepath)
    nx = utils.Nuxeo()
    scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    with open("nuxeo_item_%s.tsv"%nx.get_metadata(path=filepath)['properties']['dc:title'], encoding="utf8") as f:
        s = f.read().replace("\t", ",") + '\n' 
    sheet_id = client.open_by_url(url).id
    client.import_csv(sheet_id, s)
    os.remove("nuxeo_item_%s.tsv"%nx.get_metadata(path=filepath)['properties']['dc:title'])
if 'O' in choice and 'https' not in url:
    object_level(filepath)
if 'I' in choice and 'https' not in url:
    item_level(filepath)
if 'O' in choice and 'https' in url:
    google_object(filepath, url)
if 'I' in choice and 'https' in url:
    google_item(filepath, url)
