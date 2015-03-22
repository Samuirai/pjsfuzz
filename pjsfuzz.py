#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re

class ansi:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

motd = ansi.RED+ansi.BOLD+"""
      __    __
     /  `--´  \\
    |  |  __|  | 
    |  | |____/   """+ansi.END+ansi.BOLD+"""pjsFuzz - Fuzzing in Pajamas"""+ansi.RED+"""
    |__|     |    
      |______|
      """+ansi.END

class pjsfuzz:
    def __init__(self, name="missigno", debug=False):
        """pjsFuzz main class. Create an instance with a name, set different attributes.
        Once you set attributes, generate a fuzzing html file with write_html"""
        self.debug = debug
        if debug:
            self.log("!", "DEBUG mode active")
        
        self.name = name
        self.description = ""
        self.instance_id = hex(random.randint(0x000000,0xffffff))[2:]
        self.generation_number = 1

        self.init_template()

        self.log("-", "pjsFuzz initiated name: %s id: %s" % (self.name, self.instance_id))
        self.log("",motd)

    def init_template(self):
        """init the template related values. If multiple htmls are created, 
        this should be called to reset each round"""
        attributes = {}
        attributes['header'] = "<!-- you should set jsfuzz.attributes['header'] -->"
        attributes['body'] = "<!-- you should set jsfuzz.attributes['body'] -->" 
        attributes['script'] = "<!-- you should set jsfuzz.attributes['script'] -->" 
        
        self.debug_injection = """<script>
            console.log=function(m){
                parent.postMessage(m, "*");
            }
            window.console=console;
            </script>"""
        self.template = {}
        self.template['attributes'] = attributes
        self.template['base'] = open("templates/basic.html").read()


    def log(self, severity, msg):
        """logging functionallity. Use different severity strings (! * - : > ?) 
        to create nice colorful output"""
        if severity=='!':
            severity = ansi.RED+"[!]"+ansi.END
        elif severity=='*':
            severity = ansi.GREEN+"[*]"+ansi.END
        elif severity=='-':
            severity = ansi.BLUE+"[-]"+ansi.END
        elif severity==':':
            severity = ansi.PINK+"[:]"+ansi.END
        elif severity=='>':
            severity = ansi.BOLD+"[>]"+ansi.END
        elif severity=='?':
            severity = ansi.YELLOW+"[?]"+ansi.END
        elif severity=='':
            severity = ''
        log_msg = "%s %s" % (severity, msg)
        print log_msg

    def generate_html(self):
        """generate html based on the template and the attributes"""
        attributes = dict(self.template['attributes'])
        html = self.template['base']
        for key, val in attributes.items():
            if key not in html:
                self.log("?", "'%s' is defined, but is not in the html template" % (key))
            html = html.replace("{{%s}}" % key, val)
        html = html.replace("{{debug_injection}}", self.debug_injection)
        html = html.replace("{{name}}", self.name)
        html = html.replace("{{description}}", self.description)
        unused_template_strings = re.search(r"{{([a-zA-Z0-9_]+)}}", html)
        if unused_template_strings:
            for name in unused_template_strings.groups():
                self.log("?", "'%s' is in the template, but not in the fuzz class" % (name))
        self.log("*", "html generated")
        return html.encode('utf8')

    def write_html(self):
        """generates a html and writes it into a file. filename is determined by 
        instance_id, generation number and name"""
        filename = "fuzz_files/debug_%s.html" % self.name
        if not self.debug:
            filename = "fuzz_files/%s_%06d_%s.html" % (self.instance_id, self.generation_number, self.name)
        file_out = open(filename, 'w')
        html = self.generate_html()
        file_out.write(html)
        file_out.close()
        self.log("*", "fuzzing file '%s' written" % filename)
        self.generation_number += 1
        return html

    def done(self):
        """print done message"""
        self.log("*", "generation done. id: %s" % self.instance_id)