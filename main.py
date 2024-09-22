import platform
import distro
import subprocess

def detect_os():
   os_name = platform.system()
   os_release = platform.release()
   os_version = platform.version()

   print(f'OS name: {os_name}')
   print(f'os_release: {os_release}')
   print(f'os_version: {os_version}')

   if distro.like():
      print(f'Linux Distribution: {distro.name()} {distro.version()}')

def firewall_on():
   # Define the path to the PowerShell script
   powershell_script = "Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled True"

   # Define the command to run the PowerShell script
   command = ["powershell", "-Command", powershell_script]

   # Run the command using subprocess
   process = subprocess.run(command, shell=True)

   # Check the return code of the process
   if process.returncode == 0:
      print("[+] FireWall ON ")
   else:
      print("[-] FireWall script failed")

def choose_to_be_notified():
   # Define the path to the PowerShell script
   powershell_script = 'Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Type DWORD -Value 1'

   # Define the command to run the PowerShell script
   command = ["powershell", "-Command", powershell_script]

   # Run the command using subprocess
   process = subprocess.run(command, shell=True)

   # Check the return code of the process
   if process.returncode == 0:
      print("[+] Notify ON ")
   else:
      print("[-] Notify script failed")

def uninstall_chromium():
   # Define the path to the PowerShell script
   powershell_script = 'Get-Package -Name "Chromium" | Uninstall-Package -Confirm:$false'

   # Define the command to run the PowerShell script
   command = ["powershell", "-Command", powershell_script]

   # Run the command using subprocess
   process = subprocess.run(command, shell=True)

   # Check the return code of the process
   if process.returncode == 0:
      print("[+] chromium uninstalled ")
   else:
      print("[-] chromium not here")


def user_add_remove():
   with open('input.txt', 'r') as file:
      lines = file.readlines()
      stuff = {}
      usrs = []
      ok = True
      for i in range(0, len(lines), 1):
         usr = lines[i].strip()
         if lines[i].strip() == "Authorized Administrators:":
            continue
         elif lines[i].strip() == "Authorized Users:":
            ok = False
            continue
         if ok:
            if i + 1 < len(lines):
               pw = lines[i + 1].strip()
               if pw[0:3] == "PW:":
                  pass1 = pw.split(":")[1].strip()
                  stuff[usr] = pass1
         else:
            usrs.append(lines[i].strip())
      print(stuff)
      print(usrs)

def main():
   detect_os()
   while True:
      print()
      print("Choose options to do: ")
      print("1. Firewall ON")
      print("2. Notify ON")
      print("3. ")
      print("4. user add/remove")
      user_input = input("Enter a number: ")
      if user_input == "1":
         firewall_on()
      elif user_input == "2":
         choose_to_be_notified()
      elif user_input == "4":
         user_add_remove()
      elif user_input == "end":
         break

main()