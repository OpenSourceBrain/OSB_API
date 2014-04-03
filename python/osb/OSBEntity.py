
class OSBEntity():
    
    def __init__(self, info_array):
        self.info_array = info_array
    
    def get_custom_field(self, cf_name):
        result = None
        #print self.info_array["custom_fields"]
        for cf in self.info_array["custom_fields"]:
            if cf['name'] == cf_name and cf.has_key('value'):  
                result = cf['value']
                if result == "": 
                    result = None
        return result
