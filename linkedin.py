from linkedin_api import Linkedin

def search_people(settings):
    linkedin = Linkedin(settings["username"], settings["password"])

    filters = ["(key:resultType,value:List(PEOPLE))"]
    if settings["searchParams"]["keywordSchool"]:
        filters.append(
            f"(key:schools,value:List({settings['searchParams']['keywordSchool']}))"
        )

    