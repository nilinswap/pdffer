import { NextPage } from "next";
import { SyntheticEvent } from "react";
import { useState } from "react";
import { hit_api } from "../utils";
import Input from "../components/input";
import Router from "next/router";
import Link from "next/link";

const Login: NextPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: SyntheticEvent) => {
    e.preventDefault();
    console.log("submit", email, password);
    let { data } = await hit_api("http://localhost:8000/auth/api/verify_login/", 'POST', { email, password }); //TODO: improve this snippet. use industry standard. 
    console.log('data', data);
    if (data.success) {
      Router.push('/');
    }
  };

  return (
    <div className="flex flex-col gap-8 ml-8 mt-16">
      <h1>Login</h1>
      <form className="flex flex-col gap-2 w-80" onSubmit={handleSubmit}>
        <Input
          type="email"
          value={email}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setEmail(e.target.value)
          }
        />
        <Input
          type="password"
          value={password}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setPassword(e.target.value)
          }
        />
        <button type="submit" className="bg-blue-500 rounded-lg p-2 w-32">
          Submit
        </button>
        <Link href="/auth/forgot_password">Forgot Password?</Link>
      </form>
    </div>
  );
};

export default Login;

// TODO:
// next_url
// redirection
// forgot_password thing
