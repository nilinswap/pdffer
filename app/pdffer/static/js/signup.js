import {hit_api, is_authenticated} from './utils.js';
document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function validate_form() {
    const repassword_input = document.getElementById('repassword-input');
    const password_input = document.getElementById('password-input');
    console.log('r, p', repassword_input.value, password_input.value);
    if (password_input.value != repassword_input.value) {
        repassword_input.setCustomValidity('Passwords do not match');
        repassword_input.reportValidity()
        return false;
    }
    else {
        repassword_input.setCustomValidity('');
    }
    return true;
}

function main() {
    // if (is_authenticated()) {
    //     window.location.replace('/');
    //     return;
    // }
    const email_input = document.getElementById('email-input');
    const password_input = document.getElementById('password-input');

    const form_input = document.getElementById('signup-form');

    async function signup(event) {
        event.preventDefault();
        if (!validate_form()) {
            console.log('invalid form');
            return;
        }
        const body = {
            email: email_input.value,
            password: password_input.value
        }
        const data = hit_api('/auth/client/create/', 'POST', body);
        let redirect_url = '/please_verify_your_email';
        if (data.status_code == 278) {
            redirect_url = data.location;
        } 
        if (data.success) {
            window.location.replace(redirect_url);
        }
    }
    form_input.addEventListener('submit', signup);
}   