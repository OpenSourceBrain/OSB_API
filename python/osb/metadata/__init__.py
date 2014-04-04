"""
    Work in progress towards extracting structured metadata from OSB projects
    
    Contact p.gleeson if you are interested in using this. Subject to change without notice!!
    
"""

INDENT = "    "

class Metadata():
    rdfs = []
    
    
class RDF():
    
    def __init__(self, comment = None):
        self.comment = comment
        self.descriptions = []
    
    def to_xml(self, indent=""):
        xml = indent + '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bqmodel="http://biomodels.net/model-qualifiers/" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">\n'
        
        if self.comment:
            xml += indent + INDENT + '<!-- %s -->\n'%self.comment
              
        for description in self.descriptions:
            xml += description.to_xml(indent+INDENT)
                   
        xml += indent + "</rdf:RDF>\n" 
        
        return xml
    
class Description():
    
    def __init__(self, about):
        self.about = about
        self.qualifiers = []
        self.comment = None
    
    def to_xml(self, indent=""):
        xml = indent + '<rdf:Description rdf:about="%s">\n'%self.about
        if self.comment:
            xml += indent  + INDENT + '<!-- %s -->\n'%self.comment
              
        for qualifier in self.qualifiers:
            xml += qualifier.to_xml(indent+INDENT)
                   
        xml += indent + "</rdf:Description>\n"
              
        return xml
    
    
class Qualifier():
    
    def __init__(self, type, qualifier):
        self.type = type
        self.qualifier = qualifier
        self.resources = []
        self.comment = None
        
    def to_xml(self, indent=""):
        xml = indent + "<%s:%s>\n" % (self.type, self.qualifier) + \
              indent + INDENT + "<rdf:Bag>\n"
        if self.comment:
            xml += indent + INDENT + INDENT + '<!-- %s -->\n'%self.comment
        for resource in self.resources:
            xml += indent + INDENT + INDENT + '<rdf:li rdf:resource="%s"/>\n'%resource
                   
        xml += indent + INDENT + "</rdf:Bag>\n" + \
              indent + "</%s:%s>\n" % (self.type, self.qualifier)
              
        return xml
    

def add_simple_qualifier(description, type, qualifier, resource, comment=None):
    bq = Qualifier(type,qualifier)
    bq.resources.append(resource)
    if comment: 
        bq.comment = comment
    description.qualifiers.append(bq)


if __name__ == '__main__':

    rdf = RDF("Top level...")
    desc = Description("xyx")
    rdf.descriptions.append(desc)
    
    desc.comment ="This is a comment"
    bq = Qualifier('bqbiol','isVersionOf')
    bq.resources.append('http://identifiers.org/bto/BTO:0000131')
    bq.comment = 'Testing'
    desc.qualifiers.append(bq)

    print(rdf.to_xml())