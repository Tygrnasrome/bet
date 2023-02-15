class Filter():
    min_date = ""
    max_date = ""
    min_time = 0
    max_time = 0
    date_to = ""
    date_from = ""
    time_to = 0
    time_from = 0
    hodnoceni_from = 1
    hodnoceni_to = 1
    language_dict = {1:True}

    tag_dict = {0:"on",1:True}

    name = 0

class Palette():
    base = '#d18829'
    selected = '#a56c22'
    hover = '#92601e'
    text = '#dee4e9'
    header = '#d18023'
    body = '#2b2b2b'
    divone = '#555555'
    divtwo = '#4b4b4b'
    divthree = '#3b3b3b'
    def_base = '#d18829'
    def_selected = '#a56c22'
    def_hover = '#92601e'
    def_text = '#dee4e9'
    def_header = '#d18023'
    def_body = '#2b2b2b'
    def_divone = '#555555'
    def_divtwo = '#4b4b4b'
    def_divthree = '#3b3b3b'

class UI():
    active = 'home'
    logged_id = -1

error_dict = {'name':0, 'jazyk_id':0,'popis':0,'hodnoceni':0,'date':0,'time_spent':0}