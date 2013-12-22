import win32com.client
import sys

def schtask():
    TriggerTypeTime = 1
    ActionTypeExec = 0
    service = win32com.client.Dispatch("Schedule.Service")
    service.Connect()
    rootFolder = servcie.GetFolder("\\")
    taskDefinition = service.NewTask(0)
    regInfo = taskDefinition.RegistrationInfo
    regInfo.Description = "start liuy"
    regInfo.Author = "liuyang1"
    principal = taskDefinition.Principal
    principal.LogonType = 3
    settings = taskDefinition.Settings
    settings.Enabled = True
    settings.StartWhenAvailabel = True
    settings.Hidden = False
    settings.MultipleInstances = 0
    triggers = taskDefinition.Triggers
    trigger = triggers.Create(TriggerTypeTime)
    time = datetime.now() + timedelta(0,30)
    startTime = time.strftime("%Y-%m-%dT%H:%M:%S")
    time = datetime.now() + timedelta(0, 5*30)
    endTime = time.strftime("%Y-%m-%dT%H:%M:%S")
    print startTime
    print endTime
    trigger.StartBoundary = startTime
    trigger.EndBoundary = endTime
    trigger.ExecutionTimeLimit = "PT5M"
    trigger.Endabled = True
    Action = taskDefinition.Actions.Create(ActionTypeExec)
    Action.Path = "C:\\Windows\\System32\\notepad.exe"
    print "task definition created"
    print "abount to submit the task..."
    rootFolder.RegistrationTaskDefinition("Tesk Time Trigger",taskDefinition,6,None,None,3)
    print "Task submitted"

def testSchTask():
    schtask()

if __name__ == "__main__":
    testSchTask()
