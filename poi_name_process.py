in_file = open('', 'r')
out_file = open('', 'w')
for line in in_file:
    out_file.write(line.strip()[1:-1]+'\n')
