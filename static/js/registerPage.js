window.addEventListener('load', () => {
    const $recaptcha = document.querySelector('#g-recaptcha-response');
    if ($recaptcha) {
      $recaptcha.setAttribute('required', 'required');
    }
  })

document.getElementById("picture-input")?.addEventListener("change", function() {
    picture_preview();
})

document.getElementById("register-form")?.addEventListener("submit", function(e) {
    if (!validate_form()) {
         e.preventDefault();
    }
})

function picture_preview() {
    const picture_input = document.getElementById("picture-input");
    const preview_image = document.getElementById("preview-img");

    if (!picture_input || !preview_image)
      throw new Error("picture input or preview image not found");

    if (picture_input.files && picture_input.files[0]) {
        let reader = new FileReader();
        reader.onload = function(e) {
            preview_image.src = e.target?.result;
        };
        reader.readAsDataURL(picture_input.files[0]);
        preview_image.style.display = "block";
    }
    else {
        preview_image.src = "#";
        preview_image.style.display = "none";
    }
}

function validate_form() {
    let error_text = document.getElementById("message-text");
    let name_input = document.getElementById("name-input");
    let email_input = document.getElementById("email-input");
    let password_input = document.getElementById("password-input");
    let phone_input = document.getElementById("phone-number-input");
    let confirm_password_input = document.getElementById("confirm-password-input");
    let picture_input = document.getElementById("picture-input");

    if (!name_input || !error_text || !email_input || !password_input || !phone_input || !confirm_password_input)
        return false;

    error_text.style.color = "#fe3e3e";
    // validate email
    if (!is_valid_name(name_input.value)) {
        error_text.textContent = "Full name is not valid.";
        return false;
    }
    if (!is_valid_email(email_input.value)) {
        error_text.textContent = 'Email address is invalid.';
        return false;
    }
    // validate password
    if (!is_valid_password(password_input.value)) {
        error_text.textContent = 'Password is invalid.';
        return false;
    }
    // validate phone number
    if (!is_valid_phone_number(phone_input.value)) {
        error_text.textContent = "Phone number is invalid.";
        return false;
    }
    // validate password matching
    if (!is_password_matching(confirm_password_input.value, password_input.value)) {
        error_text.textContent = "Password did not match.";
        return false;
    }
    // validate picture
    if (!is_valid_picture(picture_input)) {
        error_text.textContent = "Profile picture is not valid.";
        return false;
    }

    error_text.textContent = "";
    return true;
}

function is_valid_name(name) {
    let name_regex = /^[A-Za-z -]+$/
    if (!name_regex.test(name)) { return false; }
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

function is_valid_phone_number(phone_number) {
    let phone_number_regex = /\d{1,13}/
    if (!phone_number_regex.test(phone_number)) { return false; }
    return true;
}

function is_password_matching(confirm_password, password) {
    if (confirm_password ===  password) { return true; }
    return false;
}

function is_valid_picture(picture) {
    let allowed_extensions = ['png', 'jpg', 'jpeg', 'gif'];
    let max_size = 1000 * 1000;

    let file_name = picture.files[0].name;
    let file_size = picture.files[0].size;
    let file_ext = file_name.split('.').pop().toLowerCase();

    if (!allowed_extensions.includes(file_ext)) { return false; }
    if (file_size > max_size) { return false; }
    return true;
}
