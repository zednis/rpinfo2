import pandas
import json
from bs4 import BeautifulSoup
import re

courses_csv = "courses-list-2016-04-24_20.25.23.xlsx"
programs_csv = "programs-list-2016-04-24_20.27.21.xlsx"


def get_metadata(id):
    return {"index": {"_index": "rpinfo2", "_type": "course", "_id": id}}


def get_course_level(code):
    digit = int(code[0])

    if digit >= 5:
        return "Graduate"
    else:
        return "Undergraduate"


def get_courses():
    df = pandas.read_excel("resources/" + courses_csv, sheetname='Worksheet')

    courses = []

    when_offered = set()
    credit_hours = set()
    prefixes = set()

    for index, row in df.iterrows():
        if row["Name"] is not pandas.np.nan:

            _prefixes = row["Prefix"].strip().upper().split(" OR ")
            _code = row["Code"]

            for prefix in _prefixes:

                prefixes.add(prefix)

                _id = prefix + "-" + _code
                subject_code = prefix + " " + _code

                course = {"id": _id,
                          "title": row["Name"],
                          "prefix": prefix,
                          "code": _code,
                          "subjectCode": subject_code,
                          "level": get_course_level(_code)}

                if row["Department Name"] is not pandas.np.nan:
                    department = {"name": row["Department Name"]}
                    course["department"] = department

                if row["School/College Name"] is not pandas.np.nan:
                    school = {"name": row["School/College Name"]}
                    course["school"] = school

                # TODO program?

                if row["Course Type"] is not pandas.np.nan:
                    course["courseType"] = row["Course Type"].strip()

                if row["Description (Rendered no HTML)"] is not pandas.np.nan:
                    course["description"] = row["Description (Rendered no HTML)"]

                if row["When Offered:"] is not pandas.np.nan:
                    course["whenOffered"] = row["When Offered:"].strip()
                    when_offered.add(row["When Offered:"].strip())

                if row["Credit Hours:"] is not pandas.np.nan:
                    course["creditHours"] = row["Credit Hours:"].strip()
                    credit_hours.add(row["Credit Hours:"].strip())

                if row["Prerequisites/Corequisites: (Rendered no HTML)"] is not pandas.np.nan:
                    # TODO parse prerequisites/corequisites text
                    course["prerequisites_corequisites"] = row["Prerequisites/Corequisites: (Rendered no HTML)"]

                if row["Cross Listed:"] is not pandas.np.nan:
                    # TODO parse crosslisted text
                    course["crossListed"] = row["Cross Listed:"]

                courses.append(course)

    # print(when_offered)
    # print(len(when_offered))
    # print(credit_hours)
    # print(prefixes)
    # print(len(prefixes))

    return courses


def get_programs():
    df = pandas.read_excel("resources/" + programs_csv, sheetname='Worksheet')

    programs = []
    for index, row in df.iterrows():
        program = {"name": row["Program Name"].strip()}

        if row["Degree Type"] is not pandas.np.nan:
            program["degree_type"] = row["Degree Type"].strip()

        if row["Program Type"] is not pandas.np.nan:
            program["program_type"] = row["Program Type"].strip()

        if row["Entity Name"] is not pandas.np.nan:
            program["department"] = row["Entity Name"].strip()

        if row["Cores"] is not pandas.np.nan:
            cores = get_program_core_courses(row["Cores"].strip())
            program["core_courses"] = list(cores)

        programs.append(program)

    return programs


def get_program_core_courses(html):
    core_courses = set()
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile("[A-Z]{4}\s[0-9]{4}")

    for line_item in soup.find_all('li'):
        text = line_item.text
        for match in pattern.findall(text):
            core_courses.add(match)

    return core_courses


def main():
    courses = get_courses()
    programs = get_programs()

    for program in programs:
        for core_course in program["core_courses"]:
            matches = [_course for _course in courses if _course["subjectCode"] == core_course]
            for course in matches:
                if "core_for" not in course:
                    course["core_for"] = []
                course["core_for"].append(program)

    data = []
    for course in courses:
        _id = course["id"]
        data.append(json.dumps(get_metadata(_id)))
        data.append(json.dumps(course))

    with open("out.bulk", "w") as bulk_file:
        bulk_file.write('\n'.join(data)+'\n')

    # print(json.dumps(get_programs()))
    # print(get_program_core_courses(open("resources/CompSciCores.html")))

if __name__ == "__main__":
    main()
