def get_users_by(nickname, first_name, last_name, db, Users, HTTPException, status):
    users = None
    if nickname is not None and first_name is None and last_name is None:
        users = db.query(Users).filter(Users.nickname == nickname, Users.is_active).all()
    elif first_name is not None and nickname is None and last_name is None:
        users = db.query(Users).filter(Users.first_name == first_name, Users.is_active).all()
    elif last_name is not None and nickname is None and first_name is None:
        users = db.query(Users).filter(Users.last_name == last_name, Users.is_active).all()
    elif nickname is not None and first_name is not None and last_name is None:
        users = db.query(Users).filter(Users.nickname == nickname, Users.first_name == first_name,
                                       Users.is_active).all()
    elif first_name is not None and last_name is not None and nickname is None:
        users = db.query(Users).filter(Users.first_name == first_name, Users.last_name == last_name,
                                       Users.is_active).all()
    elif nickname is not None and last_name is not None and first_name is None:
        users = db.query(Users).filter(Users.nickname == nickname, Users.last_name == last_name,
                                       Users.is_active).all()
    elif nickname is not None and first_name is not None and last_name is not None:
        users = db.query(Users).filter(Users.nickname == nickname, Users.first_name == first_name,
                                       Users.last_name == last_name, Users.is_active).all()
    elif nickname is None and first_name is None and last_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please fill in at least one field")

    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not found")

    return users
