from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from colorama import init, Fore, Back, Style #for colourization

#let's start with variables

subId     = "<subscription-id-of-the-resource>"
rgroup    = "<resource-group-where-resource-exists"
vmname    = None

#let's get the auth object

def auth():
    credentials=DefaultAzureCredential()
    return credentials

#lets interact with compute client

def compute(credentials=auth()):
    compute=ComputeManagementClient(credentials,subId)
    return compute

#lets get the number of VMs deployed in a resource group
#user=input("Please Select the VM number from the list below that you wish to start. Please be mindful about the chosen number.")

def getvms(compute=compute()):
    getvms=compute.virtual_machines.list(rgroup) 
    #for item in getvms:
    #    print(item)
    i=1
    vm_list=[]
    for vms in getvms:
        vm_list.append(vms.name)
        print(f"{i}.", vms.name)
        i+=1
    #print the list stored in vm_list object
    #print(f"VMlist: {vm_list}")
    return vm_list   

#get the VM name from the user input number.

def vmselection(total_vms):
    value = int(user) - 1
    #print(type(value))
    if int(user) >= 1:
        vmname=total_vms[value]
        print(Fore.GREEN + f"Your selected VM per the input provided:{vmname}")
        return vmname
    else:
        print(Fore.RED + f"process exited due to the wrong input. Pleae check and try again.")            
                   
#check VM state
def state(selected_vm):
    client=compute()
    instanceview=client.virtual_machines.instance_view(rgroup,selected_vm)
    instanceviewlist=[] #create a list
    for status in instanceview.statuses:
        instanceviewlist.append(status.code)
    #print(iview)
    if instanceviewlist[1] == 'PowerState/running':
        print(Fore.RED + "ERROR:" + f"{selected_vm} virtual-machine is already UP and running")
        exit
    else:
        print(f"VM was stopped. \nPowering On the {selected_vm} virtual machine")
        #execute start function after this
        start(selected_vm)
                
#after getting the VM name start it
def start(selected_vm):
    client=compute()
    #for debugging: print(f"VM:",vmname)
    client.virtual_machines.begin_start(rgroup,selected_vm)
    print(f"{selected_vm} Virtual Machine Started")

if __name__ == "__main__":
    print(f"Please select the number from the below input to start a virtual machine.")
    total_vms = getvms() # first value
    user=input()
    selected_vm = vmselection(total_vms) # second value
    state(selected_vm)
