"""Define and handle materials"""

import shlex

class Material:
    """Define a material"""

    def __init__(self, name="dummy"):
        self._name = name
        self.density = 0
        self.composition = "Al"
        self.comment = "(by artistlib)"

    @property
    def name(self):
        """Getter for name"""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for name"""
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = str(value)

    @property
    def definition(self):
        """Return an entry for aRTist's material list"""
        return self.name+' {density '+str(self.density)+' composition {'+str(self.composition)+'} comment {'+str(self.comment)+'}}'

    def add(self, junction):
        """Add/update this material in aRTist"""
        junction.send('dict set ::Materials::MatList '+self.definition)
        junction.send('Engine::ClearMaterials')

    def delete(self, junction):
        """Delete this material in aRTist"""
        junction.send('dict unset ::Materials::MatList '+self.definition)
        junction.send('Engine::ClearMaterials')

    def names(self, junction):
        """List the materials known to aRTist"""
        list = junction.send('dict keys $::Materials::MatList')
        return shlex.split(brace_to_quotes(list))

    def pick(self, junction, name):
        """Get an material from aRTist"""
        list = self.names(junction)
        if name in list:
            mat = junction.send('dict get $::Materials::MatList '+name)
            mat = shlex.split(brace_to_quotes(mat))
            mat = dict(zip(mat[::2], mat[1::2]))
            self._name = name
            self.density = mat['density']
            self.composition = mat['composition']
            self.comment = ''
            if 'comment' in mat:
                self.comment = mat['comment']
            return name
        else:
            return ''


# helpers

import re

def brace_to_quotes(text):
    """Helper to handle TCL dictionaries"""
    return re.sub(r'\{([^}]+)\}', r'"\1"', text)

