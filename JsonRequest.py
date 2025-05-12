import json

def create_job_description_payload():
    job_title= input("enter job title: ")
    job_info=input("please input a job description: ")
    experience = input("Please enter required experience: ")
    context=input("please enter some context ")
    
    qualification = input("Please enter your qualification: ")
    
    
    info= {
        "job title":job_title,
        "job_description": job_info,
        "experience":experience,
        "context":context,
        "qualification":qualification
        
        
    }
    


    
    
    json_payload = json.dumps(info, indent=2)
    return json_payload
print(create_job_description_payload())
