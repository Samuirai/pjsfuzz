#!/usr/bin/env python
from pjsfuzz import pjsfuzz

pjs = pjsfuzz("utf8_comment_escape", debug=False)

for i in range(0x00, 0xff):
    pjs.log(">","gen unicode %x00-%xff" % (i,i))
    scripts = ""
    pjs.template['attributes'] = {}
    testcases=[]
    for j in range(0x00, 0xff):
        unic = (i<<8)+j
        testcases.append("<script>\n<!--%s console.log('testcase 0: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\n//%s console.log('testcase 1: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\n-->%s console.log('testcase 2: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<svg%sonload=console.log('testcase 3: %s') ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<svg onload%s=console.log('testcase 4: %s') ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<svg onload=%sconsole.log('testcase 5: %s') ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.log(%stestcase 6: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.log('testcase 7: %s%s);\n</script>" % (hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log(%stestcase 8: %s\");\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.log(\"testcase 9: %s%s);\n</script>" % (hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log(%stestcase 10: %s%s);\n</script>" % (unichr(unic), hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log('testcase 11: %s%s);\n</script>" % (hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log%s'testcase 12: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.log%s('testcase 13: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.%slog('testcase 14: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole%s.log('testcase 15: %s');\n</script>" % (unichr(unic), hex(unic)))
    for testcase in testcases:
        scripts+="%s\n" % testcase
    name = "%x00-%xff" % (i,i)
    pjs.template['attributes']['body'] = "%s\n\n%s" % (scripts, name)
    pjs.template['attributes']['header'] = ""
    pjs.template['attributes']['script'] = ""
    pjs.write_html()
pjs.done()