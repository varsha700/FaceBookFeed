function Validate()
{
    user = document.getElementById("username").value;
    pass = document.getElementById("password").value;

    err = document.getElementById("err");
    err1 = document.getElementById("err1");

    if(user.length ==0)
    {
        err.innerHTML="*Plz enter username!!";
        err.style.color="red";
    }
    else{err.innerHTML="";}

}