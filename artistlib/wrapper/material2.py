from .artist_send import ArtistSend
import shlex
import re


class MaterialService(ArtistSend):
    def add_material(
        self,
        m_name: str = "dummy",
        density: float = 0,
        composition: str = "Al",
        comment: str = "(by artistlib)",
    ):
        self._control_number(density)
        self._control_str(m_name, composition, comment)
        a = ""
        a += self.send(
            "dict set ::Materials::MatList "
            + str(m_name)
            + " {density "
            + str(density)
            + " composition {"
            + str(composition)
            + "} comment {"
            + str(comment)
            + "}}"
        )
        a += self.send("Engine::ClearMaterials")
        self.send(("::Materials::RefreshTable"))
        return a

    def delete_material(self, m_name: str):
        self._control_str(m_name)
        a = self.send("dict unset ::Materials::MatList " + str(m_name))
        self.send(("::Materials::RefreshTable"))
        return a

    def _brace_to_quotes(self, text):
        """Helper utilities for working with Tcl dictionaries."""
        return re.sub(r"\{([^}]+)\}", r'"\1"', text)

    def names_material(self):
        mat_list = self.send(("dict keys $::Materials::MatList"))
        return shlex.split(self._brace_to_quotes(mat_list))

    def pick_material(self, mname):
        """Retrieves a material definition from aRTist."""
        list = self.names_material()
        if mname in list:
            mat = self.send("dict get $::Materials::MatList " + mname)
            mat = shlex.split(self._brace_to_quotes(mat))
            mat = dict(zip(mat[::2], mat[1::2]))
            if "comment" in mat:
                return mname, mat["density"], mat["composition"], mat["comment"]
            return mname, mat["density"], mat["composition"]
        else:
            return ""


class Material:
    def __init__(self, name="dummy"):
        self._name = name
        self.density = 0
        self.composition = "Al"
        self.comment = "(by artistlib)"

    def add(self):
        M = MaterialService()
        return M.add_material(
            m_name=self._name,
            density=self.density,
            composition=self.composition,
            comment=self.comment,
        )

    def delete(self):
        M = MaterialService()
        return M.delete_material(m_name=self._name)

    def pick(self, name):
        M = MaterialService()
        ans = M.pick_material(name)
        if ans == "":
            return ""
        self.comment = ""
        if len(ans) == 4:
            self.comment = ans[3]
        self.density = ans[1]
        self.composition = ans[2]
        return name
