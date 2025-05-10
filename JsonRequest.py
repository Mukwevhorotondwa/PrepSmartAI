import json

def create_job_description_payload(user_input):
    job_info= input("enter job title: ")
    job_info=input("please input a job description: ")
    experience = input("Please enter required experience: ")
    
    
    job_info= {
        "job_description": user_input.strip()
        
        
    }
    context=input("please enter some context")
    background_info_about_me=input("Enter your cv infomartion this is to,make ressponses to be relative to you")
    qualification = input("Please enter your qualification: ")

    # Convert dictionary to JSON string (pretty printed)
    
    print("...............................................")
    json_payload = json.dumps(payload, indent=2)
    return json_payload
