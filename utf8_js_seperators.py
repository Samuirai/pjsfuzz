#!/usr/bin/env python
from pjsfuzz import pjsfuzz

pjs = pjsfuzz("utf8_js_seperators", debug=False)
pjs.desc = "Test which characters are allowed between js functions"

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
        testcases.append("<script>\nconsole.log(%stestcase 0: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.log('testcase 1: %s%s);\n</script>" % (hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log(%stestcase 2: %s\");\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.log(\"testcase 3: %s%s);\n</script>" % (hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log(%stestcase 4: %s%s);\n</script>" % (unichr(unic), hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log%s'testcase 5: %s'%s;\n</script>" % (unichr(unic), hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log('testcase 6: %s%s);\n</script>" % (hex(unic), unichr(unic)))
        testcases.append("<script>\nconsole.log%s'testcase 7: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.log%s('testcase 8: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.%slog('testcase 9: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole%s.log('testcase 10: %s');\n</script>" % (unichr(unic), hex(unic)))
        testcases.append("<script>\nconsole.log('testcase 11: %s');%sasd!@#$</script>" % (unichr(unic), hex(unic)))
    for testcase in testcases:
        scripts+="%s\n" % testcase
    name = "%x00-%xff" % (i,i)
    pjs.template['attributes']['body'] = "%s\n\n%s" % (scripts, name)
    pjs.write_html()
pjs.done()

"""
results:
> testcase 8: 0xa0    | <script>\nconsole.log\u00a0('executed');\n</script>
> testcase 8: 0x1680
> testcase 8: 0x180e
> testcase 8: 0x2000
> testcase 8: 0x2001
> testcase 8: 0x2002
> testcase 8: 0x2003
> testcase 8: 0x2004
> testcase 8: 0x2005
> testcase 8: 0x2006
> testcase 8: 0x2007
> testcase 8: 0x2008
> testcase 8: 0x2009
> testcase 8: 0x200a
> testcase 8: 0x2028
> testcase 8: 0x2029
> testcase 8: 0x202f
> testcase 8: 0x205f
> testcase 8: 0x3000
> testcase 9: 0xa0    | <script>\nconsole.\u00a0log('executed');\n</script>
> testcase 9: 0x1680
> testcase 9: 0x180e
> testcase 9: 0x2000
> testcase 9: 0x2001
> testcase 9: 0x2002
> testcase 9: 0x2003
> testcase 9: 0x2004
> testcase 9: 0x2005
> testcase 9: 0x2006
> testcase 9: 0x2007
> testcase 9: 0x2008
> testcase 9: 0x2009
> testcase 9: 0x200a
> testcase 9: 0x2028
> testcase 9: 0x2029
> testcase 9: 0x202f
> testcase 9: 0x205f
> testcase 9: 0x3000
> testcase 10: 0xa0    | <script>\nconsole\u00a0.log('executed');\n</script>
> testcase 10: 0x1680
> testcase 10: 0x180e
> testcase 10: 0x2000
> testcase 10: 0x2001
> testcase 10: 0x2002
> testcase 10: 0x2003
> testcase 10: 0x2004
> testcase 10: 0x2005
> testcase 10: 0x2006
> testcase 10: 0x2007
> testcase 10: 0x2008
> testcase 10: 0x2009
> testcase 10: 0x200a
> testcase 10: 0x2028
> testcase 10: 0x2029
> testcase 10: 0x202f
> testcase 10: 0x205f
> testcase 10: 0x3000
"""