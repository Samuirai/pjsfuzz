#!/usr/bin/env python
from pjsfuzz import pjsfuzz

pjs = pjsfuzz("utf8_comment_escape", debug=False)
pjs.desc = "Test which characters break out of a javascript comment"

for i in range(0x00, 0xff):
    pjs.log(">","gen unicode %x00-%xff" % (i,i))
    scripts = ""
    pjs.init_template()
    testcases=[]
    for j in range(0x00, 0xff):
        unic = (i<<8)+j
        # ignore standard ascii stuff
        if unic<0x7f:
            continue
        testcases.append("<script>\n<!--%s console.log('testcase 0: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\n//%s console.log('testcase 1: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\n-->%s console.log('testcase 2: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\n/*%s console.log('testcase 3: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\n/*%s console.log('testcase 4: %s');*/\n</script>" % (unichr(unic), hex(unic)))
    for testcase in testcases:
        scripts+="%s\n" % testcase
    name = "%x00-%xff" % (i,i)
    pjs.template['attributes']['body'] = "%s\n\n%s" % (scripts, name)
    pjs.write_html()
pjs.done()

"""
result:
> testcase 0: 0x2028 | <!--\u2028console.log('executed')
> testcase 0: 0x2029
> testcase 1: 0x2028 | //\u2028console.log('executed')
> testcase 1: 0x2029
> testcase 2: 0x2028 | -->\u2028console.log('executed')
> testcase 2: 0x2029 
"""