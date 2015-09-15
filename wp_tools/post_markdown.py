#!/usr/bin/python
# PYTHON_ARGCOMPLETE_OK
from os                                         import environ                  as os_environ
from sys                                        import path                     as py_path
py_path.append(                                 os_environ['HOME'] + '/.scripts')
from system_argparse                            import *
from subprocess                                 import Popen                    as sub_popen
from subprocess                                 import PIPE                     as sub_PIPE
from re                                         import sub                      as re_sub

def cleanup_grip(html_file):
    with open(html_file,'r') as f:
        html                                = f.read()

    T                                       =   '<div class="comment-body markdown-body markdown-format">'
    A                                       =   html
    A                                       =   A[:A.find(T)].replace('\n','').replace('<p>','').replace('</p>','') + A[A.find(T):]

    r                                       =   ['<div class="preview-page">',
                                                '<div class="container">',
                                                '<div class="repository-with-sidebar repo-container ">',
                                                '<div class="discussion-timeline wide">',
                                                '<div class="timeline-comment-wrapper">',
                                                '<div class="timeline-comment">',
                                                '<div class="comment">',
                                                '<div class="comment-content">']
    B                                       =   '<div>&nbsp;</div>'

    for it in r:
        A  = A.replace(it,'')
        pt = A.rfind(B)
        A  = A[ : A[:pt].rfind('</div>') ] + A[ A[:pt].rfind('</div>') + len('</div>') : pt ] + A[pt:]

    pt = A.rfind(B)
    pt1= A[:pt].rfind('</p>')
    pt2= pt + A[pt:].rfind('</div>')
    A  = A[:pt1] + A[pt1:pt2].replace('\n','') + A[pt2:].replace('\n','').replace('</br>','').replace('<p>','').replace('</p>','')
    A  = A.replace('<div>&nbsp;</div>','')

    with open(html_file,'w') as f:
        f.write(A)
    return True

@arg('-i','--input',
        help='content to post \nNOTE: input can also be piped')
@arg('-t','--title',default=parse_choices_from_exec('date +%Y.%m.%d').strip('\n'),
        help='title of paste')
@arg('---',dest='input')
def post_to_wordpress(args):
    """convert markdown, clean up html, post to wordpress"""
    convert_cmd                             =   "grip --gfm --export --wide %s 2>&1"
    post_cmd                                =   "wp post create %s --post_title='%s'"

    if hasattr(args,'input'):
        (_out,_err)                         =   sub_popen(convert_cmd % args.input,stdout=sub_PIPE,
                                                    shell=True).communicate()
        assert _out.count('Exporting to ')
        args.html_file                      =   _out.replace('Exporting to ','').strip('\n')

    res                                     =   cleanup_grip(args.html_file)
    assert res==True

    (_out,_err)                             =   sub_popen(post_cmd % (args.html_file,args.title),
                                                    stdout=sub_PIPE,shell=True).communicate()

    print 'Posted!'



import sys
if __name__ == '__main__':
    global input_text

    if not sys.stdin.isatty():
        import fileinput
        fd_stdin,input_text                     =   fileinput.input('-'),[]
        while True:
            f_descr_1                           =   fd_stdin.fileno()
            line                                =   ''.join([seg for seg in fd_stdin.readline()])
            f_descr_2                           =   fd_stdin.fileno()
            if f_descr_1==f_descr_2==-1 or fd_stdin.lineno()==0:
                break
            if line:
                # print line
                input_text.append(                  line)
        input_text                              =   ''.join(input_text).strip('\n')
        run_custom_argparse({'input_text':input_text})
    else:
        run_custom_argparse()
