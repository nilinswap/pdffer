import {is_authenticated} from './utils.js';
import AuthForm from './auth_form.js';


document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function main() {
    is_authenticated().then(logged_in => {
        if (logged_in === true) {
            window.location.replace('/');
             return;
        }
    });
    const auth_form = new AuthForm('login-form', '/auth/verify_login/', '/');
    auth_form.registerSubmit().then(
        () => {
            console.log('registered');
        }
    ).catch(
        (err) => {
            console.log('login err', err);
        }
    );


}