import {hit_signup_login_api} from './utils.js';

document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function main() {
    const email_input = document.getElementById('email-input');
    const password_input = document.getElementById('password-input');
    const form_input = document.getElementById('signup-form');

    async function signup(event) {
        event.preventDefault();
        const email = email_input.value;
        const password = password_input.value;
        hit_signup_login_api( email, password, '/auth/client/create/', '/please_verify_your_email');
    }

    form_input.addEventListener('submit', signup);
}   