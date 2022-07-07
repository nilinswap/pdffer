console.log("hello world!");


document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function main() {
    const email_input = document.getElementById('email-input');
    const password_input = document.getElementById('password-input');
    const form_input = document.getElementById('signup-form');



    form_input.addEventListener('submit', hit_create_client_api);
    async function hit_create_client_api(event) {
        console.log("here")
        event.preventDefault();
        const email = email_input.value;
        const password = password_input.value;
        const response = await fetch('/auth/client/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        const data = await response.json();
        console.log(data);
        if (data.success) {
            window.location.href = '/please_verify_your_email';
        } else {
            alert(data.message);
        }
    }

}