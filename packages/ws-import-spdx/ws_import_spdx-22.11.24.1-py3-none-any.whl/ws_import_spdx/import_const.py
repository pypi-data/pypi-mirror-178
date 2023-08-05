from enum import Enum


class SHA1CalcType(Enum):
    maven = ("y","JAVA","jar") #jar
    gradle = ("y","JAVA","jar") #jar
    maven_1 = ("y","JAVA","war") #war
    gradle_1 = ("y","JAVA","war") #war
    npm = ("y","NPM","js") # js
    cdnjs = ("y","CDNJS","js") # js
    bower = ("y","BOWER","jar") #jar
    pypi = ("n","PYTHON","whl") #whl
    cargo = ("n","Crate","crate") #crate
    cocoapods = ("n","CocoaPods","")
    pub = ("n","Pub","pub") #pub
    nuget = ("y","NUGET","ng") #ng
    opam = ("n","Opam","opam") #opam
    composer = ("n","PHP","php") #php
    cran = ("n","R","r") #r
    gem = ("y","RUBY","gem") #gem
    hackage = ("y","Cabal","cabal") #cabal
    rpm = ("n","RPM","rpm") #rpm
    hex = ("y","HEX","hex") #hex, h86
    dotnet = ("y","NUGET","exe") #exe

    @property
    def lower_case(self):
        return self.value[0]

    @property
    def language(self):
        return self.value[1]

    @property
    def ext(self):
        return self.value[2]

    @classmethod
    def get_package_type(cls, f_t: str):
        return cls.__dict__[f_t]

    @classmethod
    def get_package_type_list_by_ext(cls, ext: str):
        res = []
        for el_ in cls:
            if el_.ext == ext:
               res.append(el_)
        return res