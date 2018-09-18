
# used to store info of professors


class Faculty:
    personal_info = dict()

    def __init__(self):
        self.personal_info['page'] = list()
        self.personal_info['department'] = list()
        self.personal_info['title'] = list()
        self.personal_info['email'] = list()
        self.personal_info['phone'] = list()
        self.personal_info['name'] = list()

    def edit_info(self, page, name, department, title, email, phone):
        self.personal_info['page'].append(page)
        self.personal_info['department'].append(department)
        self.personal_info['title'].append(title)
        self.personal_info['email'].append(email)
        self.personal_info['phone'].append(phone)
        self.personal_info['name'].append(name)

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


# used for describe papers
class Paper:
    def __init__(self):
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

