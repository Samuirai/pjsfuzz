#!/usr/bin/env python
from pjsfuzz import pjsfuzz

pjs = pjsfuzz("utf8_img_tag_seperator", debug=False)
pjs.desc = "Test which characters are allowed between stuff in img tags"

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
        testcases.append("<img %sonerror='console.log(\"testcase 0: %s\")' src >\n" % (unichr(unic), hex(unic)))
        testcases.append("<img onerror%s='console.log(\"testcase 1: %s\")' src >\n" % (unichr(unic), hex(unic)))
        testcases.append("<%simg onerror='console.log(\"testcase 2: %s\")' src >\n" % (unichr(unic), hex(unic)))
        testcases.append("<img onerror=%s'console.log(\"testcase 3: %s\")' src >\n" % (unichr(unic), hex(unic)))
        testcases.append("<img onerror='%sconsole.log(\"testcase 4: %s\")' src >\n" % (unichr(unic), hex(unic)))
        testcases.append("<img onerror='console.log(\"testcase 5: %s\")%s' attr=val src >\n" % (hex(unic), unichr(unic)))
        testcases.append("<img onerror='console%s.log(\"testcase 6: %s\")' src >\n" % (unichr(unic), hex(unic)))
        testcases.append("<img onerror='console.%slog(\"testcase 7: %s\")' src >\n" % (unichr(unic), hex(unic)))
        testcases.append("<img onerror='console.log%s(\"testcase 8: %s\")' src >\n" % (unichr(unic), hex(unic)))
    for testcase in testcases:
        scripts+="%s\n" % testcase
    name = "%x00-%xff" % (i,i)
    pjs.template['attributes']['body'] = "%s\n\n%s" % (scripts, name)
    pjs.write_html()
pjs.done()

"""
results:
> testcase 4: 0xa0    | <img onerror='\u00a0console.log("executed")' src >
> testcase 4: 0x1680
> testcase 4: 0x180e
> testcase 4: 0x2000
> testcase 4: 0x2001
> testcase 4: 0x2002
> testcase 4: 0x2003
> testcase 4: 0x2004
> testcase 4: 0x2005
> testcase 4: 0x2006
> testcase 4: 0x2007
> testcase 4: 0x2008
> testcase 4: 0x2009
> testcase 4: 0x200a
> testcase 4: 0x2028
> testcase 4: 0x2029
> testcase 4: 0x202f
> testcase 4: 0x205f
> testcase 4: 0x3000
> testcase 5: 0xa0    | <img onerror='console.log("executed")\u00a0' src >
> testcase 5: 0x1680
> testcase 5: 0x180e
> testcase 5: 0x2000
> testcase 5: 0x2001
> testcase 5: 0x2002
> testcase 5: 0x2003
> testcase 5: 0x2004
> testcase 5: 0x2005
> testcase 5: 0x2006
> testcase 5: 0x2007
> testcase 5: 0x2008
> testcase 5: 0x2009
> testcase 5: 0x200a
> testcase 5: 0x2028
> testcase 5: 0x2029
> testcase 5: 0x202f
> testcase 5: 0x205f
> testcase 5: 0x3000
> testcase 6: 0xa0    | <img onerror='console\u00a0.log("executed")' src >
> testcase 6: 0x1680
> testcase 6: 0x180e
> testcase 6: 0x2000
> testcase 6: 0x2001
> testcase 6: 0x2002
> testcase 6: 0x2003
> testcase 6: 0x2004
> testcase 6: 0x2005
> testcase 6: 0x2006
> testcase 6: 0x2007
> testcase 6: 0x2008
> testcase 6: 0x2009
> testcase 6: 0x200a
> testcase 6: 0x2028
> testcase 6: 0x2029
> testcase 6: 0x202f
> testcase 6: 0x205f
> testcase 6: 0x3000
> testcase 7: 0xa0    | <img onerror='console.\u00a0log("executed")' src >
> testcase 7: 0x1680
> testcase 7: 0x180e
> testcase 7: 0x2000
> testcase 7: 0x2001
> testcase 7: 0x2002
> testcase 7: 0x2003
> testcase 7: 0x2004
> testcase 7: 0x2005
> testcase 7: 0x2006
> testcase 7: 0x2007
> testcase 7: 0x2008
> testcase 7: 0x2009
> testcase 7: 0x200a
> testcase 7: 0x2028
> testcase 7: 0x2029
> testcase 7: 0x202f
> testcase 7: 0x205f
> testcase 7: 0x3000
> testcase 8: 0xa0    | <img onerror='console.log\u00a0("executed")' src >
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
"""