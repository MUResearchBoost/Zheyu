import csv
import json
import re
# used to store info of professors

# get rid of special punctuation
def remove_duplicateid(authors):
    for person in authors:
        author = person
    return author

def filtering_words(text):
    s = re.sub("[\'\\\\/\"\\n]", "", text)
    return s

def differentiate_affiliation(affiliation):
    mu = ['University of Missouri', 'Mizzou', 'University of Missouri-Columbia']
    if int(affiliation['affiliation-id']) != 60006173:
        notice = 0
    else:
        for element in mu:
            if affiliation['affiliation-name'].find(element) != -1:
                notice = 1
            else:
                notice = 0
    return notice

class Faculty:
    personal_info = dict()

    def __init__(self):
        self.personal_info['page'] = list()
        self.personal_info['department'] = list()
        self.personal_info['title'] = list()
        self.personal_info['email'] = list()
        self.personal_info['phone'] = list()
        self.personal_info['name'] = list()
        self.personal_info['author_id'] = None
        self.personal_info['eid'] = None

    def edit_info(self, page, name, department, title, email, phone):
        self.personal_info['page'].append(page)
        self.personal_info['department'].append(department)
        self.personal_info['title'].append(title)
        self.personal_info['email'].append(email)
        self.personal_info['phone'].append(phone)
        self.personal_info['name'].append(name)

    def id_edit(self, i, j):
        if j == 'author_id':
            self.personal_info['author_id'] = i
            return 0
        else:
            self.personal_info['eid'] = i
            return 1

    def restore_data(self, data, filename):
        with open(filename, 'w') as f:
            for element in data:
                f.write(element)
                f.write('\n')
        self.log('Saved file %s' % filename)

# used for extract data from database


class ReadFile:
    name = list()
    def txt(self, address):
        with open(address, 'r', encoding='utf-8') as file:
            line = file.readline()
            while line:
                self.name.append(line)
                line = file .readline()
            file.close()
        return self.name

    def scisearch(self, name):
        modified_name = list()
        for letter in name:
            if letter == ' ':
                modified_name.append("%20")
            else:
                modified_name.append(letter)
        return ''.join(modified_name)

    def get_affiliation(self, address):
        w = dict()
        name = list()
        affiliation = list()
        with open(address, 'r') as f:
            reader = csv.reader(f)
            for rows in reader:
                if len(rows) == 2:
                    name.append(rows[0])
                    affiliation.append(rows[1])
                elif len(rows) == 1:
                    name.append(rows[0])
                    affiliation.append('None')
                elif len(rows) > 2:
                    name.append(rows[0])
                    affiliation.append(rows[1] + rows[2])
        w['name'] = name
        w['affiliation'] = affiliation
        return w

# used for describe papers
class Paper:
    def IEEE_data(self, result):
        data = result
        collection = list()
        keys = ['article_number', 'publication_number']
        value = [data['article_number'], data['publication_number']]
        otherid = dict(zip(keys, value))
        maintitle = data['title']
        subtitle = 'None'
        abstact_content = filtering_words(data['abstract'])
        content = 'None'
        references = list()
        references.append("None")
        #url_key = ['pdf_url', 'abstract_url']
        #url_value = [data['pdf_url'], data['abstract_url']]
        original_url = data['pdf_url']
        citation = list()
        citation.append('None')
        for terms_type in data['index_terms'].values():
            #i = terms_type
            #j = terms_type['terms']
            for terms in terms_type['terms']:
                collection.append(terms)
        publishdate = ''
        submitdate = ''
        #publishdata = data['conference_dates']
        #submitdate = data['conference_dates']
        publisher =list()
        for author_list in data['authors'].values():
            for author in author_list:
                publisher.append(author['full_name'])
        language = 'English'
        publication_type = data['content_type']
        keys_entire = ['otherId', 'mainTitle', 'subTitle', 'abstractContent', 'content', 'references', 'originUrl',
                       'citation', 'collections', 'publishDate', 'submitDate', 'publisher', 'language', 'publicationType']
        value_entire = [otherid, maintitle, subtitle, abstact_content, content, references, original_url, citation, collection, publishdate, submitdate, publisher, language, publication_type]
        data_modified = dict(zip(keys_entire, value_entire))
        return data_modified

    def scopus_data(self, data):
        collection = list()
        item = data['item']
        bibrecord = item['bibrecord']
        item_info = bibrecord['item-info']
        itemid = item_info['itemid']
        keys = ['ce:pii', 'ce:doi']
        value = [itemid['ce:pii'], itemid['ce:doi']]
        otherid = dict(zip(keys, value))

        head = bibrecord['head']
        maintitle = head['citation-title']
        subtitle = 'None'
        abstact_content = filtering_words(head['abstracts'])
        content = 'None'
        references = list()
        references.append("None")
        # url_key = ['pdf_url', 'abstract_url']
        # url_value = [data['pdf_url'], data['abstract_url']]
        coredata = data['coredata']
        links = coredata['link']
        firsthref = links[0]
        originUrl = firsthref['@href']

        citation = list()
        citation.append('None')


        subjectareas = data['subject-areas']
        subjectarea = subjectareas['subject-area']
        for area in subjectarea:
            collection.append(area['$'])

        publishdate = ''
        submitdate = ''
        # publishdata = data['conference_dates']
        # submitdate = data['conference_dates']

        publisher = list()
        author = data['authors']
        for a in author.value():
            preferred_name = a['preferred_name']

        language = 'English'
        publication_type = coredata['subtypeDescription']

        keys_entire = ['otherId', 'mainTitle', 'subTitle', 'abstractContent', 'content', 'references', 'originUrl',
                       'citation', 'collections', 'publishDate', 'submitDate', 'publisher', 'language',
                       'publicationType']
        value_entire = [otherid, maintitle, subtitle, abstact_content, content, references, originUrl, citation,
                        collection, publishdate, submitdate, publisher, language, publication_type]
        data_modified = dict(zip(keys_entire, value_entire))



    def __init__(self):
        self.paper_list = list()
        self.title = None
        self.author = None
        self.abstract = None
        self.source = None
        self.page_link = None
        self.journal_name = None
        self.faculty = None


    def get_new_paper(self, title, author, abstract, source, link, journal, faculty):
        self.title = title
        self.author = author
        self.abstract = abstract
        self.source = source
        self.page_link = link
        self.journal_name = journal
        self.faculty = faculty


class ClusteringPaper(Paper):
    personal_collection = dict()
    journal_collection = dict()
    corporation = list()

    def author_pub(self, paper):
        mu_author = paper.faculty
        if mu_author in self.personal_collection:
            self.personal_collection[mu_author].append(paper)
        else:
            self.personal_collection[mu_author] = list()
            self.personal_collection[mu_author].append(paper)

    def journal_pub(self, paper):
        journal = paper.journal_name
        if journal in self.journal_collection:
            self.journal_collection[journal].append(paper)
        else:
            self.journal_collection[journal] = list()
            self.journal_collection[journal].append(paper)

    def get_collection(self, choice):
        if choice is "person":
            return self.personal_collection
        else:
            return self.journal_collection


