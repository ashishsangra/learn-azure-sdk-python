from azure.mgmt.compute import ComputeManagementClient
from azure.identity     import DefaultAzureCredential
import re

#declare variables

subid="<resoruce-subscription-id" #flag: required value

#authentication object
def authclient():
    authentication=DefaultAzureCredential()
    return authentication

#define computeclient object

def computeclient():
    authentication=authclient()
    computeclient=ComputeManagementClient(authentication,subid)
    return computeclient
    
#now we got the compute client in return from above function #lets try to build a logic to search for the resource group from the VMs list

#lets use this compute object for next

def listvms():
    compute=computeclient()
    list_vms=compute.virtual_machines.list_all()
    #list_all will return a paginated response. so iterate over it
    #declare a list
    vm_list=[]
    num = 0
    #In the line for vms in list_vms:, the variable vms represents each virtual machine object returned by the list_vms iterator. 
    # Then, vm_list.append(vms.id) adds the ID of each virtual machine to the vm_list list.
    for vms in list_vms:
        vm_list.append(vms.id)
        num+=1
    return vm_list

#print VM resource ids
#len(my_list) function returns the current length of the my_list list, 
#and the for loop iterates over the indices of the list, from 0 to len(my_list) - 1.
def vmids(vm_list):
    print(f"Please find below the virtual machine's resource Ids in the current subscription: {subid}\n")
    #use print for debuging only. print(f"length:", len(vm_list))
    j=1
    display_vm_ids=""
    for i in range(len(vm_list)):
        #only for debugging use print commands: 
        #all_vm_ids=vm_list[i]
        #print(f"{j}.",all_vm_ids)
        display_vm_ids+=f"{j}.{vm_list[i]}\n"
        j+=1
    #print(f"TEST:\n",display_vm_ids)
    return display_vm_ids 
               
#now i need to create a function which will actually use regex as pattern match to get the VMs and the resource group from the above vm_list output        

def match(vm_list):
    matchpattern= r'\/subscriptions\/.*\/resourceGroups\/(.*)\/providers\/Microsoft\.Compute\/virtualMachines\/(.*)'
    #only for debugging print(f"test:",display_vm_ids)
    #iterate through each line in display_vm_ids
    vm_match=[]
    for vms in vm_list:
        match=re.fullmatch(matchpattern,vms)
        #print only for debugging, print(f"{match.group(1)}, {match.group(2)}")
        resourcegroup=match.group(1)
        vmname=match.group(2)
        print(f"{resourcegroup},{vmname}")
        test=f"{resourcegroup},{vmname}"
        vm_match.append(test) #add match one by one in list vm_list
    return vm_match    #return the list
    
#let's get to the final work now. starting the vm command which need resource group name of the vm and vm name
#def start():
        
def start(user,vm_match,compute):
    #use print only for debugging #print(f"TESTUSER:",user)
    pattern=r'(.*)\,({})'.format(user) #print(f"TESTPATTERN:",pattern)
    #list vm_match only for debugigng #print(f"vm_match:",vm_match)
    searchmatch = re.findall(pattern,"\n".join(vm_match))
    #print(f"TESTMATCH:",searchmatch)
    resourcegroup=str(searchmatch[0])
    #print(f"RG:",resourcegroup)
    #print(f"RGTYPE:",type(resourcegroup))
    pattern=r'\(\'(.*)\'\,\s\'.*\'\)'
    #print(f"new pattern:",pattern)
    rgroup=re.fullmatch(pattern,resourcegroup)
    print(f"resourcegroup:",rgroup[1])
    print(f"vmname:",user)
    resourcegroup=rgroup[1]
    vmname=user
    print(f"Starting Virtual machine:",vmname)
    compute.virtual_machines.begin_start(resourcegroup,vmname).result
            
if __name__ == "__main__":
    compute=computeclient()
    vm_list=listvms()
    display_vm_ids=vmids(vm_list)
    vm_match=match(vm_list)
    print("\n")
    user=input(str("Enter the VM name:"))
    start(user,vm_match,compute)
