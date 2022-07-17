import {hit_api, is_authenticated} from './utils.js';

document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function main() {
    // if (is_authenticated()) {
    //     window.location.replace('/');
    //     return;
    // }

    const email_input = document.getElementById('email-input');
    const password_input = document.getElementById('password-input');
    const form_input = document.getElementById('login-form');

    async function login(event) {
        event.preventDefault();
        const body = {
            email: email_input.value,
            password: password_input.value
        }
        const data = hit_api('/auth/verify_login/', 'POST', body);
        let redirect_url = '/';
        if (data.status_code == 278) {
            redirect_url = data.location;
        }
        if (data.success) {
            window.location.replace(redirect_url);
        }
    }
    form_input.addEventListener('submit', login);
}