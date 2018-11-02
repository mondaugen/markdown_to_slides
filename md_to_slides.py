import re
import sys

def change_ending(s,split='.',ending='.html'):
    return ".".join(s.split(split)[:-1])+ending

if len(sys.argv) < 2:
    sys.stderr.write("args are markdown_file [html_header_file]\n")
    sys.exit()

input_file_name = sys.argv[1]
header_contents=None
if len(sys.argv) >= 3:
    header_file_name = sys.argv[2]
    with open(header_file_name,'r') as f:
        header_contents=f.read()

re_slide_break = re.compile('# SLIDE (.*)$')

slide_file_name_list=[]
slide_num=0

with open(input_file_name) as f:
    first_line = f.readline()
    title_match = re_slide_break.match(first_line)
    # Force there to be a first slide
    title = title_match.groups()[0] if title_match is not None else ''
    path='.'.join(input_file_name.split('.')[:-1])+'%d.md'%(slide_num,)
    slide_file_name_list.append(
    dict(title=title,path=path))
    cur_out_file = open(path,'w')
    if header_contents is not None:
        cur_out_file.write(header_contents)
    slide_num += 1
    cur_out_file.write('<title>'+title + "</title>\n")
    cur_out_file.write("# " + title + "\n")
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        title_match = re_slide_break.match(line)
        if title_match is not None:
            path='.'.join(input_file_name.split('.')[:-1])+'%d.md'%(slide_num,)
            slide_file_name_list.append(
            dict(title=title_match.groups()[0],path=path))
            slide_num += 1
            cur_out_file.close()
            cur_out_file=open(path,'w')
            if header_contents is not None:
                cur_out_file.write(header_contents)
            cur_out_file.write('<title>\n'+title_match.groups()[0] + "\n</title>\n")
            cur_out_file.write("# " + title_match.groups()[0] + "\n")
        else:
            cur_out_file.write(line)

# Close last file
cur_out_file.close()

        



# write previous links
for i, slide_file in enumerate(slide_file_name_list[1:]):
    with open(slide_file['path'],'a') as cur_out_file:
        cur_out_file.write('[<](%s)\n' % (change_ending(slide_file_name_list[i]['path']),))

# Write links to all files
for i,slide_file in enumerate(slide_file_name_list):
    with open(slide_file['path'],'a') as cur_out_file:
        for j, other_slide_file in enumerate(slide_file_name_list):
            if i != j:
                #cur_out_file.write('[%d](%s)\n' % (j+1,change_ending(other_slide_file['path']),))
                cur_out_file.write('[(%d) %s](%s)\n' % (j+1,other_slide_file['title'],change_ending(other_slide_file['path']),))

# write next links
for i,slide_file in enumerate(slide_file_name_list[:-1]):
    with open(slide_file['path'],'a') as cur_out_file:
        cur_out_file.write('[>](%s)\n' % (change_ending(slide_file_name_list[i+1]['path']),))

