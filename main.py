import platform
import subprocess

def detect_os():
   os_name = platform.system()
   os_release = platform.release()
   os_version = platform.version()

   print(f'OS name: {os_name}')
   print(f'os_release: {os_release}')
   print(f'os_version: {os_version}')
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
   command_list = ['Import-Module PackageManagement', 'Get-Package -Name "Chromium" | Uninstall-Package -Confirm:$false', 'Get-Package -Name "CCleaner" | Uninstall-Package -Confirm:$false', 'Get-Package -Name "DriverUpdate" | Uninstall-Package -Confirm:$false', 'Get-Package -Name "Babylon" | Uninstall-Package -Confirm:$false']
   # Define the path to the PowerShell script
   for i in range(len(command_list)):
      command = ["powershell", "-Command", command_list[i]]
      process = subprocess.run(command, shell=True)
   # Check the return code of the process
      if process.returncode == 0:
         print("[+] " + command_list[i])
      else:
         print("[-] " + command_list[i])

#removes a false user
def remove_user(username):
   command = f"net user {username} /DELETE"
   subprocess.run(["powershell", "-Command", command], check=True)

#adds people to admin
def add_new_admin(admin,password):
   command = f"net user {admin},{password} /ADD"
   command = f"net localgroup Administrators {admin} /ADD"
   subprocess.run(["powershell", "-Command", command], check=True)

#adds people to users
def add_new_user(username):
   command = f"net user {username} /ADD"
   subprocess.run(["powershell", "-Command", command], check=True)

def user_add_remove():
   administrators = []
   authorized_users = []
   passwords = []
   with open("input.txt", "r") as file:
      lines = file.readlines()
   in_users_section = False
   for line in lines[1:]:  # skip the first line
      line = line.strip()
      if line == "Authorized Users:":
         in_users_section = True
         continue
      if in_users_section:
         authorized_users.append(line)
      else:
         if line.startswith("PAS:"):
            passwords.append(line[4:])
         else:
            administrators.append(line)
   print("Authorized Users:", authorized_users)
   print()
   print("Authorized Administrators:", administrators)
   print()
   print("Passwords:", passwords)
   # Create a dictionary to map administrators to their passwords
   admin_passwords = {}
   for admin, password in zip(administrators, passwords):
      admin_passwords[admin] = password
   print("Map of Admins --> passwords:", admin_passwords)
   #adds all the users
   for user in authorized_users:
      add_new_user(user)
   #adds all the admins and their passwords
   for admin, password in admin_passwords.items():
      add_new_admin(admin,password)


   command = "powershell -Command Get-LocalUser | Select-Object -ExpandProperty Name"
   existing_users_output = subprocess.check_output(command, shell=True).decode()
   existing_users = existing_users_output.split()
   #removes all non-users





def controlPanelStuff():
   control_panel_commands = {
      'system': 'control /name Microsoft.System',
      'programs': 'control /name Microsoft.ProgramsAndFeatures',
      'network': 'control /name Microsoft.NetworkAndSharingCenter',
      'display': 'control /name Microsoft.Display',
      'sound': 'control /name Microsoft.Sound',
      'user_accounts': 'control /name Microsoft.UserAccounts',
      'devices': 'control /name Microsoft.DevicesAndPrinters'
   }
   try:
      subprocess.run("control /name Microsoft.SystemAndSecurity", shell = True)
      print("opened System and Security ")
      subprocess.run("explorer ms-actioncenter:", shell = True)
      print("Opened Action Center.")
      subprocess.run("powershell -Command \"Install-WindowsUpdate -AcceptAll -AutoReboot\"", shell = True)
      shutil.copytree("C:\\Data", "D:\\Backup")
      subprocess.run("powershell -Command \"Start-MpScan -ScanType FullScan\"", shell=True)
   except Exception as e:
      print(f"failed to open 'system and security'/Action Center: {e}")

def main():
   detect_os()
   while True:
      print()
      print("Choose options to do: ")
      print("1. Firewall ON")
      print("2. Notify ON")
      print("3. program unintall")
      print("4. user add/remove")
      user_input = input("Enter a number: ")
      if user_input == "1":
         firewall_on()
      elif user_input == "2":
         choose_to_be_notified()
      elif user_input == "3":
         uninstall_chromium()
      elif user_input == "4":
         user_add_remove()
      elif user_input == "end":
         break
main()