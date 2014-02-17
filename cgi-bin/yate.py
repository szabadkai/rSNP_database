#!/usr/bin/env python3

from string import Template
import os

def start_response(resp="text/html"):
    return('Content-type: ' + resp + '\n')

def include_header(the_title):
    with open('../templates/header.html') as headf:
        head_text = headf.read()
    header = Template(head_text)
    return(header.substitute(title=the_title)+'<div class="container">')

def add_script(url):
    return('<script type="text/javascript" src="'+ url +'"></script>')

def include_footer(the_links):
    with open('../templates/footer.html') as footf:
        foot_text = footf.read()
    link_string = ''
    for key in the_links:
        link_string += '<a href="' + the_links[key] + '">' + key + '</a>&nbsp;&nbsp;&nbsp;&nbsp;'
    footer = Template(foot_text)
    return('</div>'+footer.substitute(links=link_string))

def start_form(the_url, form_type="POST"):
    return('<form action="' + the_url + '" method="' + form_type + '">')

def end_form(submit_msg="Submit"):
    return('<p></p><input type=submit value="' + submit_msg + '"></form>')

def radio_button(rb_name, rb_value):
    return('<input type="radio" name="' + rb_name +
                             '" value="' + rb_value + '"> ' + rb_value + '<br />')

def field(rb_name, rb_value):
    return('<input type="text" name="' + rb_name +
                             '" value="' + rb_value + '"> ' + rb_value + '<br />')
def u_list(items):
    u_string = '<ul>'
    for item in items:
        u_string += '<li>' + item + '</li>'
    u_string += '</ul>'
    return(u_string)

def header(header_text, header_level=2):
    return('<h' + str(header_level) + '>' + header_text +
           '</h' + str(header_level) + '>')

def para(para_text):
    return('<p>' + para_text + '</p>') 

def table(table_list):
    for row in table_list:
        print "<thead>"
        for col in sorted(row.keys()):
            print "<th>%s</th>" % col
        print "</thead>"
        print "<tr>"
        for col in sorted(row.keys()):
            print "<th>%s</th>" % row[col]
        print "</tr>"
