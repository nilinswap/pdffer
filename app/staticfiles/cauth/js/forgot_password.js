import {is_authenticated} from './utils.js';
import AuthForm from './auth_form.js';

document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function validate_form() {
    const repassword_input = document.getElementById('repeat-new-password-input');
    const password_input = document.getElementById('new-password-input');
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
    is_authenticated().then(logged_in => {
        if (logged_in) {
            alert("You should not see this page, if you are logged in. Please contact the administrator.");
            if (logged_in === true) {
                window.location.replace('/');
                return;
            }
        }
    });
    const auth_form = new AuthForm('forgot-password-form', '/auth/forgot_password/', '/reset_password_success', validate_form);
    auth_form.registerSubmit().then(
        () => {
            console.log('registered');
        }
    ).catch(
        (err) => {
            console.log('forget password err', err);
        }
    );
}