

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


