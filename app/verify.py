import re
import pickle
import random
####################################    User Authentication Function   #####################################

def name_valid(name):
    if name.isalpha() and len(name) > 2:
        return True
    else:
        return False

def password_valid(pass1):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
	
	# compiling regex
    pat = re.compile(reg)
	
	# searching regex				
    mat = re.search(pat, pass1)
	
	# validating conditions
    if mat:
        return True
    else:
        return False

def password_check(password1, password2):
    if password1 == password2:
        return True
    else : 
        return False

def contact_valid(number):
    Pattern = re.fullmatch("[6-9][0-9]{9}",number)
    if Pattern != None:
        return True
    else:
        return False

def authentication(first_name, last_name, pass1, pass2):
    if name_valid(first_name) == False:
        return "Invalid First Name"           
    elif name_valid(last_name) == False:
            return "Invalid Last Name"
    elif password_valid(pass1) == False:
        return "Password Should be in Proper Format. (eg. Password@1234)"
    elif password_check(pass1, pass2) == False:
        return "Password Not Matched"
    else:
        return "success"
    
    #########################################################################################################
def review_prediction(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15):
    list1 = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15]
    # Load the model from a file
    with open("models/feedback_predict.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/feedback_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    
    external_review_vect = scaler.transform([list1])
    feedback = model.predict(external_review_vect)[0]
    return feedback

def suggest_doctor():
    dics = [{'Dr B S V Prasad': 'XR3P+JQP, Falak Complex, Nashik Pune Road, Above Archies Gallery, Nashik, Maharashtra 422001.'},
            {'Dr. Priya Rajhans': 'Rajendra Colony, Police Station, Shastri Path, opp. Badshah Hotel, opp. Nasik Road, Rajwada Nagar, Nashik Road, Nashik, Maharashtra 422101.'},
            {'Dr.Jyoti Ugale': 'Business Plus, C-202, near Sai Square, Mumbai Naka, Gaikwad Nagar, Nashik, Maharashtra 422002.'},
            {'Dr Anup Bharati': '102, First Floor, Samraat Nucleus, Between Radiant Plus Hosp & Sahyadri Hospital, near Dadasaheb Gaikwad Sabhagruh, Mumbai Naka, Dr.Homi Bhabha Nagar, Nashik, Maharashtra 422001.'}
            ]
    return random.choice(dics)