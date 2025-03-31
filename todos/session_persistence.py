from uuid import uuid4

class SessionPersistence:
    def __init__(self, session):
        self.session = session
        if 'lists' not in self.session['lists']:
            self.session['lists'] = []
    
    def find_list(self, list_id):
        found = (lst for lst in self.session['lists'] if lst['id'] == list_id)
        return next(found, None)
    
    def all_lists(self):
        return self.session['lists']
    
    def create_new_list(self, title):
        lists = g.storage.all_lists()
        lists.append({
            'id': str(uuid4()),
            'title': title,
            'todo': []
        })
        self.session.modified = True