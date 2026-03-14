@app.post("/login")
def login(request: Request, username: str = Form(""), password: str = Form("")):

    if username.strip() == "" or password.strip() == "":

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "something fishy going on please check username / password"
            }
        )

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user:

        user = models.User(
            username=username,
            password=password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    response = RedirectResponse("/dashboard", status_code=303)

    response.set_cookie("user_id", str(user.id))
    response.set_cookie("username", username)

    return response
