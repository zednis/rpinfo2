import pandas
import json

courses_csv = "courses-list-2016-04-24_20.25.23.xlsx"
programs_csv = "programs-list-2016-04-24_20.27.21.xlsx"


def get_metadata(id):
    return {"index": {"_index": "rpinfo2", "_type": "course", "_id": id}}


def get_courses():
    df = pandas.read_excel("resources/" + courses_csv, sheetname='Worksheet')

    courses = []

    for index, row in df.iterrows():
        if row["Name"] is not pandas.np.nan:

            _id = row["Prefix"] + "-" + row["Code"]
            subject_code = row["Prefix"] + " " + row["Code"]

            course = {"id": _id,
                      "title": row["Name"],
                      "prefix": row["Prefix"],
                      "code": row["Code"],
                      "subjectCode": subject_code}

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

            if row["Credit Hours:"] is not pandas.np.nan:
                course["creditHours"] = row["Credit Hours:"].strip()

            if row["Prerequisites/Corequisites: (Rendered no HTML)"] is not pandas.np.nan:
                # TODO parse prerequisites/corequisites text
                course["prerequisites_corequisites"] = row["Prerequisites/Corequisites: (Rendered no HTML)"]

            if row["Cross Listed:"] is not pandas.np.nan:
                # TODO parse crosslisted text
                course["crossListed"] = row["Cross Listed:"]

            courses.append(course)

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
