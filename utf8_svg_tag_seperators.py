#!/usr/bin/env python
from pjsfuzz import pjsfuzz

pjs = pjsfuzz("utf8_svg_tag_seperators", debug=False)
pjs.desc = "Test which characters are allowed between stuff between svg tags"

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
        testcases.append("<svg %sonload='console.log(\"testcase 0: %s\")' ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<svg onload%s='console.log(\"testcase 1: %s\")' ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<%ssvg onload='console.log(\"testcase 2: %s\")' ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<svg onload=%s'console.log(\"testcase 3: %s\")' ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<svg onload='%sconsole.log(\"testcase 4: %s\")' ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<svg onload='console.log(\"testcase 5: %s\")%s' attr=val ></svg>\n" % (hex(unic), unichr(unic)))
        testcases.append("<svg onload='console%s.log(\"testcase 6: %s\")' ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<svg onload='console.%slog(\"testcase 7: %s\")' ></svg>\n" % (unichr(unic), hex(unic)))
        testcases.append("<svg onload='console.log%s(\"testcase 8: %s\")' ></svg>\n" % (unichr(unic), hex(unic)))
    for testcase in testcases:
        scripts+="%s\n" % testcase
    name = "%x00-%xff" % (i,i)
    pjs.template['attributes']['body'] = "%s\n\n%s" % (scripts, name)
    pjs.write_html()
pjs.done()

"""
results:
> testcase 4: 0xa0    | <svg onload='\u00a0console.log("executed")' ></svg>
> testcase 4: 0x1680
> testcase 4: 0x180e
> testcase 4: 0x2008
> testcase 4: 0x202f
> testcase 4: 0x2003
> testcase 4: 0x2028
> testcase 4: 0x2002
> testcase 4: 0x200a
> testcase 4: 0x2009
> testcase 4: 0x2001
> testcase 4: 0x2005
> testcase 4: 0x2029
> testcase 4: 0x2006
> testcase 4: 0x2004
> testcase 4: 0x2000
> testcase 4: 0x2007
> testcase 4: 0x205f
> testcase 4: 0x3000
> testcase 5: 0xa0    | <svg onload='console.log("executed")\u00a0' attr=val ></svg>
> testcase 5: 0x1680
> testcase 5: 0x180e
> testcase 5: 0x2000
> testcase 5: 0x2028
> testcase 5: 0x202f
> testcase 5: 0x2006
> testcase 5: 0x205f
> testcase 5: 0x200a
> testcase 5: 0x2004
> testcase 5: 0x2005
> testcase 5: 0x2002
> testcase 5: 0x2007
> testcase 5: 0x2009
> testcase 5: 0x2001
> testcase 5: 0x2029
> testcase 5: 0x2008
> testcase 5: 0x2003
> testcase 5: 0x3000
> testcase 6: 0xa0    | <svg onload='console\u00a0.log("executed")' ></svg>
> testcase 6: 0x1680
> testcase 6: 0x180e
> testcase 6: 0x2004
> testcase 6: 0x2002
> testcase 6: 0x205f
> testcase 6: 0x2008
> testcase 6: 0x2006
> testcase 6: 0x2001
> testcase 6: 0x2005
> testcase 6: 0x2000
> testcase 6: 0x2007
> testcase 6: 0x200a
> testcase 6: 0x2009
> testcase 6: 0x2029
> testcase 6: 0x2028
> testcase 6: 0x202f
> testcase 6: 0x2003
> testcase 6: 0x3000
> testcase 7: 0xa0    | <svg onload='console.\u00a0log("executed")' ></svg>
> testcase 7: 0x1680
> testcase 7: 0x180e
> testcase 7: 0x2001
> testcase 7: 0x2006
> testcase 7: 0x2029
> testcase 7: 0x2004
> testcase 7: 0x202f
> testcase 7: 0x2002
> testcase 7: 0x2008
> testcase 7: 0x2028
> testcase 7: 0x2000
> testcase 7: 0x2005
> testcase 7: 0x205f
> testcase 7: 0x2009
> testcase 7: 0x200a
> testcase 7: 0x2003
> testcase 7: 0x2007
> testcase 7: 0x3000
> testcase 8: 0xa0    | <svg onload='console.log\u00a0("executed")' ></svg>
> testcase 8: 0x1680
> testcase 8: 0x180e
> testcase 8: 0x2008
> testcase 8: 0x200a
> testcase 8: 0x2009
> testcase 8: 0x205f
> testcase 8: 0x2004
> testcase 8: 0x202f
> testcase 8: 0x2001
> testcase 8: 0x2007
> testcase 8: 0x2029
> testcase 8: 0x2028
> testcase 8: 0x2003
> testcase 8: 0x2006
> testcase 8: 0x2005
> testcase 8: 0x2000
> testcase 8: 0x2002
> testcase 8: 0x3000
"""

