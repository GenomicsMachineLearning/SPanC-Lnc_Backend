import re

def parse_genomic_coordinates(search_param_str):
    if not search_param_str:
        return None, None, None

    x = re.search(
        ("^(((chr)?([1-9]|1[0-9]|2[0-2]|[XYM]|GL000\d\d\d\.1|KI270\d\d\d\.1)))"
         "(\:)?"
         "(((((\d+)\-(\d+)?)|((\d+)\+(\d+)))))?$"),
        search_param_str)

    if x:
        group2, group10, group11, group13, group14 = x.group(2, 10, 11, 13, 14)

        chromosome = group2
        start = int(group10) if group10 else None
        end = int(group11) if group11 else None

        if group13 and group14:
            start = int(group13)
            end = int(group13) + int(group14)

        return chromosome, start, end

    return None, None, None