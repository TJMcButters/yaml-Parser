import sys, os

#  Fills in the Blocks list
inHeader = True
header = []
inResources = False
inFooter = False
footer = []
blocks = []
data = []
blockTypes = []
blockTitles = []
dataInc = -1
hrf = 0
with open(sys.argv[1], 'r') as f:
    x = f.readlines()
    for line in x:

        if line.startswith("Resources:"):
            header.append(line)
            hrf = 1
            inFooter = False
            inHeader = False
            inResources = True

        if hrf == 2 and ' ' not in line and len(line.strip()) != 0:
            inHeader = False
            inResources = False
            inFooter = True

        if inHeader is True and hrf == 0:
            header.append(line)

        if inResources is True and hrf == 1:
            if line.startswith('    '):
                blocks[dataInc].append(line.strip('\n'))
                if line.startswith("    Type:"):
                    type = line.strip()
                    type = type[6:]
                    if type.startswith("\""):
                        type = type[1:-1]
                    blockTypes.append(type)
            elif line.startswith('  ') and not line.startswith('    ') and not line.startswith(
                    '      ') and not line.startswith('        '):
                dataInc += 1
                blockTitles.append(line.strip())
                blocks.append([])
                blocks[dataInc].append(line.strip('\n'))
                ti = line.strip()
            elif len(line.strip()) != 0 and ' ' in line and not line.startswith("Resources:"):
                hrf = 2
                inResources = False
                inHeader = False
                inFooter = True

        if inFooter is True and hrf == 2:
            footer.append(line)

block_with_type = zip(blockTypes, blockTitles, blocks)
block_with_type.sort(key=lambda v: (v[0].lower(), v[1].lower()))

new_blocks = []
for item in block_with_type:
    new_blocks.append(item[2])

for x in new_blocks:
    for y in x:
        print(y)
    print("\n")

f = open(sys.argv[2], "w+")
for x in header:
    for y in x:
        f.write(y)

for x in new_blocks:
    for y in x:
        f.write(y)
        f.write("\n")
    f.write("\n")

for x in footer:
    for y in x:
        f.write(y)
f.close()

sys.stdout.write(sys.argv[2])
