export default function Login() {
    return (
        <div className="container">
            <h1>Login</h1>
            <div class="col-lg-6">
                <form method="post">
                    <input name="email" id="email-input" type="email" class="form-control" placeholder="email" required />
                    <input name="password" id="password-input" type="password" class="form-control" placeholder="password" required />
                    <input type="hidden" name="next_url" value="{{ next_url }}" />
                    <span class="input-group-btn">
                        <button id="login-submit-button" class="btn btn-default" type="submit">Submit</button>
                    </span>
                    <a href="/auth/forgot_password">Forgot Password?</a>
                </form>
            </div>
        </div> 
    );
}
    

    // <form>
    //             <label htmlFor="email">Email</label>
    //             <input type="email" id="email" />
    //             <label htmlFor="password">Password</label>
    //             <input type="password" id="password" />
    //             <button type="submit">Login</button>
    //         </form>

    // TODO:
    // forgot_password thing
    // validations - email, password, required field
    // hit api and submit button
    // next_url
    // redirection
