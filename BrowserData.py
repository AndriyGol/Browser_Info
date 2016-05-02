from datetime import date
class BrowserData():
    formInput = None
    places = None
    cookies = None
    browserInfo = None
    
class HasText():
    text = None
    
class HasCount():
    count = None
    
class HasUrl():
    url = None
    host = None
    
class HasDates():
    firstUsedDate = None
    lastUsedDate = None
    
class FormInput(HasText, HasCount, HasDates):
    fieldName = None
    
class Place(HasText, HasCount, HasDates, HasUrl):
    typed = None
    hidden = None

class Cookie(HasUrl):
    name = None
    value = None
    

    