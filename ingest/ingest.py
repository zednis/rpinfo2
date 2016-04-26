import pandas
import json

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
    # print(credit_hours)
    # print(prefixes)
    # print(len(prefixes))

    return courses


def main():
    courses = get_courses()

    data = []
    for course in courses:
        _id = course["id"]
        data.append(json.dumps(get_metadata(_id)))
        data.append(json.dumps(course))

    with open("out.bulk", "w") as bulk_file:
        bulk_file.write('\n'.join(data)+'\n')


if __name__ == "__main__":
    main()
