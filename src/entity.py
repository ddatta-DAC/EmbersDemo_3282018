# an entity(instance) object
# can belong to multiple classes
class entity:

    def __init__(self, _name, _class=None):
        self._name = _name
        self._class = []
        self.set_class(_class)
        self.text_data = []
        self.tweet_text = []
        return

    def get_class(self):
        return self._class

    def display(self):
        print ' instance :: ', self._name
        return

    def set_text(self, text_data):

        if self.text_data is None:
            self.text_data = text_data
        else:
            self.text_data.append(text_data)
        return

    def set_class(self, _class):
        if _class is not None:
            self._class.append(_class)
        return

    def get_name(self):
        return self._name

    def get_text_data(self):
        return self.text_data

    def set_tweet_text(self,text):
        self.tweet_text = text

    def get_tweet_text(self):
        return self.tweet_text
