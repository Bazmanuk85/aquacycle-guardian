{% extends "base.html" %}

{% block content %}

<style>

.login-container{
display:flex;
justify-content:center;
align-items:center;
height:60vh;
}

.login-card{
background:#132c3f;
padding:40px;
border-radius:18px;
width:320px;
box-shadow:0 0 25px rgba(31,127,209,0.4);
}

.login-card input{
width:90%;
padding:12px;
margin:10px 0;
border:none;
border-radius:12px;
}

.login-card button{
width:95%;
padding:12px;
margin-top:10px;
border-radius:12px;
}

.create-account{
margin-top:15px;
font-size:14px;
}

.create-account a{
color:#6bb7ff;
text-decoration:none;
}

.error{
color:#ff6b6b;
margin-top:10px;
}

</style>


<div class="login-container">

<div class="login-card">

<h2>Login</h2>

<form method="post" action="/login">

<input type="text" name="username" placeholder="Username" required>

<input type="password" name="password" placeholder="Password" required>

<button type="submit">Login</button>

</form>

{% if error %}
<div class="error">{{error}}</div>
{% endif %}

<div class="create-account">
Don't have an account?
<br>
<a href="/register">Create one here</a>
</div>

</div>

</div>

{% endblock %}
