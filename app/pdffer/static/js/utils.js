export async function hit_signup_login_api(email, password, post_api_url, redirect_url) {
    console.log("here")
    const response = await fetch(post_api_url, {
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
    if (data.status_code == 278) {
        redirect_url = data.location
    }
    if (data.success) {
        window.location.href = redirect_url;
    }
}
