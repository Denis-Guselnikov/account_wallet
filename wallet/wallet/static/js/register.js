const usernameField=document.querySelector('#usernameField');
const feedBackArea=document.querySelector('.invalid_feedback');
const emailField=document.querySelector('#emailField');
const emailFeedBackArea=document.querySelector('.emailFeedBackArea');
const passwordField=document.querySelector('#passwordField'); 
const usernameSucceessOutput=document.querySelector('.usernameSucceessOutput');
const emailSucceessOutput=document.querySelector('.emailSucceessOutput');
const showPasswordToggle=document.querySelector('.showPasswordToggle');
const submitBtn=document.querySelector('.submit-btn');
const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "Показать Пароль") {
      showPasswordToggle.textContent = "Скрыть Пароль";
      passwordField.setAttribute("type", "text");
    } else {
      showPasswordToggle.textContent = "Показать Пароль";
      passwordField.setAttribute("type", "password");
    }
  };


showPasswordToggle.addEventListener("click", handleToggleInput);


emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    emailSucceessOutput.style.display = "block";
    emailSucceessOutput.textContent = `Checing: ${emailVal}`;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";    

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email/", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            console.log("data", data);
            emailSucceessOutput.style.display = "none";
            if(data.email_error) {                
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });
    }
});


usernameField.addEventListener("keyup", (e) => {    
    const usernameVal = e.target.value;

    usernameSucceessOutput.style.display = "block";
    usernameSucceessOutput.textContent = `Checing: ${usernameVal}`;

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";    

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username/", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {            
            usernameSucceessOutput.style.display = "none";
            if(data.username_error) {
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                submitBtn.disabled = true;                
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });
    }    
});