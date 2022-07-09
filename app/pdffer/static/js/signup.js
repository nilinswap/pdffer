import {hit_api, is_authenticated} from './utils.js';

document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function main() {
    if (is_authenticated()) {
        window.location.replace('/');
        return;
    }
    const email_input = document.getElementById('email-input');
    const password_input = document.getElementById('password-input');
    const form_input = document.getElementById('signup-form');

    async function signup(event) {
        event.preventDefault();
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