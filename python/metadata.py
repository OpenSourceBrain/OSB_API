

INDENT = "    "

class Metadata():
    rdfs = []
    
    
class RDF():
    
    
    def __init__(self, about):
        self.about = about
        self.qualifiers = []
    
    def to_xml(self, indent=""):
        xml = indent + '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bqmodel="http://biomodels.net/model-qualifiers/" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">\n' + \
              indent + INDENT + '<rdf:Description rdf:about="%s">\n'%self.about
              
        for qualifier in self.qualifiers:
            xml += qualifier.to_xml(indent+INDENT+INDENT)
                   
        xml += indent + INDENT + "</rdf:Description>\n" + \
              indent + "</rdf:RDF>\n" 
              
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


if __name__ == '__main__':

    rdf = RDF("xyx")
    bq = Qualifier('bqbiol','isVersionOf')
    bq.resources.append('http://identifiers.org/bto/BTO:0000131')
    bq.comment = 'Testing'
    rdf.qualifiers.append(bq)

    print(rdf.to_xml())