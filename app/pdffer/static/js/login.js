import {hit_api, is_authenticated} from './utils.js';

document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function main() {
    let is_auth = is_authenticated().then(logged_in => {
        if (logged_in === true) {
            window.location.replace('/');
             return;
        }
    });
    console.log("is_auth", is_auth);
    const email_input = document.getElementById('email-input');
    const password_input = document.getElementById('password-input');
    const form_input = document.getElementById('login-form');

    async function login(event) {
        event.preventDefault();
        const body = {
            email: email_input.value,
            password: password_input.value
        }
        const {data, status} = await hit_api('/auth/verify_login/', 'POST', body);
        console.log('data', data);
        window.datadata = data;
        let redirect_url = '/';
        if (status == 278) {
            redirect_url = data.location;
        }
        if (data.success) {
            window.location.replace(redirect_url);
        }
    }
    form_input.addEventListener('submit', login);
}