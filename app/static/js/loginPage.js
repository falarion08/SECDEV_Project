window.addEventListener('load', () => {
    const $recaptcha = document.querySelector('#g-recaptcha-response');
    if ($recaptcha) {
      $recaptcha.setAttribute('required', 'required');
    }
  })

document.getElementById("login-form")?.addEventListener("submit", function(e) {
    if (!validate_form()) {
        e.preventDefault();
}
})

function validate_form() {
    let error_text = document.getElementById("message-text");
    let email_input = document.getElementById("email-input");
    let password_input = document.getElementById("password-input");

    if (!error_text || !email_input || !password_input)
        return false;

    error_text.style.color = "#fe3e3e";
    // validate email
    if (!is_valid_email(email_input.value)) {
        error_text.textContent = 'Email address is invalid.';
        return false;
    }
    // validate password
    if (!is_valid_password(password_input.value)) {
        error_text.textContent = 'Password is invalid.';
        return false;
    }

    error_text.textContent = "";
    return true;
}

function is_valid_email(email) {
    let email_regex = /((?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))/;
    if (!email_regex.test(email)) { return false; }
    return true;
}

function is_valid_password(password) {
    let password_regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[`~!@#$%^&*()\-_=+\[\]\\|;:'\",<.>/?])[A-Za-z\d`~!@#$%^&*()\-_=+\[\]\\|;:'\",<.>/?]{12,64}$/
    if (!password_regex.test(password)) { return false; }
    return true;
}