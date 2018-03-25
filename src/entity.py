# an entity(instance) object
# can belong to multiple classes
class entity:

    def __init__(self, _name, _class=None):
        self._name = _name
        self._class = []
        self.set_class(_class)
        return

    def get_class(self):
        return self._class

    def display(self):
        print ' instance :: ', self._name
        return

    def set_text(self, text_dict):

        if self.text_dict is None:
            self.text_dict = text_dict
        else:
            for k, v in text_dict.iteritems():
                self.text_dict[k].append(v)
        return

    def set_class(self, _class):
        if _class is not None:
            self._class.append(_class)
        return

    def get_name(self):
        return self._name

    def get_text_dict(self):
        return self.text_dict


