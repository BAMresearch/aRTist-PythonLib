"""Define and handle materials"""

import shlex
import re


class Material:
    """Defines a material"""

    def __init__(self, name="dummy"):
        self._name = name
        self.density = 0
        self.composition = "Al"
        self.comment = "(by artistlib)"

    @property
    def name(self):
        """Returns the material name."""
        return self._name

    @name.setter
    def name(self, value):
        """Sets the material name."""
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = str(value)

    @property
    def definition(self):
        """Returns a material entry in the format required by the aRTist material list."""
        return (
            self.name
            + " {density "
            + str(self.density)
            + " composition {"
            + str(self.composition)
            + "} comment {"
            + str(self.comment)
            + "}}"
        )

    def add(self, junction):
        """Adds or updates the material in aRTist."""
        junction.send("dict set ::Materials::MatList " + self.definition)
        junction.send("Engine::ClearMaterials")

    def delete(self, junction):
        """Deletes the material from aRTist."""
        junction.send("dict unset ::Materials::MatList " + self.definition)
        junction.send("Engine::ClearMaterials")

    def names(self, junction):
        """Returns a list of all materials currently available in aRTist."""
        list = junction.send("dict keys $::Materials::MatList")
        return shlex.split(brace_to_quotes(list))

    def pick(self, junction, name):
        """Retrieves a material definition from aRTist."""
        list = self.names(junction)
        if name in list:
            mat = junction.send("dict get $::Materials::MatList " + name)
            mat = shlex.split(brace_to_quotes(mat))
            mat = dict(zip(mat[::2], mat[1::2]))
            self._name = name
            self.density = mat["density"]
            self.composition = mat["composition"]
            self.comment = ""
            if "comment" in mat:
                self.comment = mat["comment"]
            return name
        else:
            return ""


# helpers


def brace_to_quotes(text):
    """Helper functions for handling Tcl dictionaries."""
    return re.sub(r"\{([^}]+)\}", r'"\1"', text)
