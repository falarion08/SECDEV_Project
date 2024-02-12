from app.controllers import verify_password,hashPassword
from app.models.User import User,db

def create(user_email,password,phone_number,full_name):
    isPasswordValid = verify_password(password)
    

    if isPasswordValid:
        userList = User.query.filter_by(email= user_email).first()

        if(userList is None):
            hashedResult = hashPassword(password)
            new_user = User(email=user_email,hash= hashedResult[1], salt = hashedResult[0],
                            full_name = full_name,phone_number=phone_number)       
            
            db.session.add(new_user)
            db.session.commit()
            print('User added to the database')
        else:
            print('User record already exist')
    else:
        print('Password not valid')

