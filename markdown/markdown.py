import re


def get_header(line):
    """

    @param line:
    @return:
    """
    if re.match('###### (.*)', line):
        return f'<h6>{line[7:]}</h6>'
    elif re.match('##### (.*)', line):
        return f'<h5>{line[6:]}</h5>'
    elif re.match('#### (.*)', line):
        return f'<h4>{line[5:]}</h4>'
    elif re.match('### (.*)', line):
        return f'<h3>{line[4:]}</h3>'
    elif re.match('## (.*)', line):
        return f'<h2>{line[3:]}</h2>'
    elif re.match('# (.*)', line):
        return f'<h1>{line[2:]}</h1>'
    return line


def replace_tag(expression, line, tag):
    matched = re.match(expression, line)

    if matched:
        return f"{matched.group(1)}<{tag}>{matched.group(2)}</{tag}>{matched.group(3)}"
    return line


def parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False
    for line in lines:
        # replace # with headers
        i = get_header(line)

        # find all *
        matched = re.match(r'\* (.*)', i)
        if matched:
            if not in_list:
                in_list = True
                curr = replace_tag('(.*)__(.*)__(.*)', matched.group(1), 'strong')
                curr = replace_tag('(.*)_(.*)_(.*)', curr, 'em')
                i = '<ul><li>' + curr + '</li>'
            else:
                curr = replace_tag('(.*)__(.*)__(.*)', matched.group(1), 'strong')
                curr = replace_tag('(.*)_(.*)_(.*)', curr, 'em')
                i = '<li>' + curr + '</li>'
        else:
            if in_list:
                in_list_append = True
                in_list = False

        matched = re.match('<h|<ul|<p|<li', i)
        if not matched:
            i = '<p>' + i + '</p>'

        matched = re.match('(.*)__(.*)__(.*)', i)
        if matched:
            i = matched.group(1) + '<strong>' + matched.group(2) + '</strong>' + matched.group(3)

        matched = re.match('(.*)_(.*)_(.*)', i)
        if matched:
            i = matched.group(1) + '<em>' + matched.group(2) + '</em>' + matched.group(3)

        if in_list_append:
            i = '</ul>' + i
            in_list_append = False
        res += i
    if in_list:
        res += '</ul>'
    return res
