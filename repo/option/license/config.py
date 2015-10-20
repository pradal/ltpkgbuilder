def main(info, extra):
    try:
        name = extra['license']
    except KeyError:
        name = raw_input("license name:")

    try:
        year = extra['year']
    except KeyError:
        year = raw_input("year [2015]:")
        if year == "":
            year = "2015"

    try:
        organization = extra['organization']
    except KeyError:
        organization = raw_input("organization [openalea]:")
        if organization == "":
            organization = "openalea"

    try:
        project = extra['project']
    except KeyError:
        project = raw_input("project [%s]:" % info['base']['pkg_fullname'])
        if project == "":
            project = info['base']['pkg_fullname']

    return dict(name=name.strip(),
                year=year,
                organization=organization,
                project=project)
