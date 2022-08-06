import {hit_api, is_authenticated} from './utils.js';
import AuthForm from './auth_form.js';

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


function integrate_verify_email() {
    const email_input = document.getElementById('email-input');
    email_input.addEventListener('input', async function () {
        const email = email_input.value;
        const res = await hit_api(`/auth/api/verify_email?email=${email}`, 'GET');
        console.log("integrate_verify_email res", res, res.data, res.status);
        if (res.status === 200) {
            let svg = 'middle.svg'
            if (res.data.valid_email && res.data.unique_email) {
                svg = 'tick.svg';
            } else if (res.data.valid_email && !res.data.unique_email) {
                svg = 'cross.svg';
            }
            
            if (svg !== 'tick.svg') {
                email_input.setCustomValidity(res.data.message);
                email_input.reportValidity()
            }else {
                email_input.setCustomValidity('');
            }
            
            let email_svg = document.getElementById('emailsvg').getElementsByTagName('img')[0];
            email_svg.src = `/static/images/icons/${svg}`;
        }
    });
}

function main() {
    is_authenticated().then(logged_in => {
        if (logged_in === true) {
            window.location.replace('/');
             return;
        }
    });
    integrate_verify_email();
    const auth_form = new AuthForm('signup-form', '/auth/api/client/create/', '/auth/please_verify_your_email', validate_form);
    auth_form.registerSubmit().then(
        () => {
            console.log('registered');
        }
    ).catch(
        (err) => {
            console.log('signup err', err);
        }
    );
}   