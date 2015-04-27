
class OSBEntity(object):
    
    def __init__(self, info_array):
        self.info_array = info_array
    
    def get_custom_field(self, cf_name):
        result = None
        #print "Checking for %s in custom fields: %s" % (cf_name, self.info_array["custom_fields"])
        for cf in self.info_array["custom_fields"]:
            if cf['name'] == cf_name and 'value' in cf:  
                result = cf['value']
                if result == "": 
                    result = None
        return result
