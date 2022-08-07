document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function main() {
    console.log('base_generic');
}

function logOut() {
    fetch('/auth/logout/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => {
        console.log('res')
        if (res.status === 200) {
            window.location.replace('/');
        }
    });
}