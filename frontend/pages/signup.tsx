import { NextPage } from "next";
import { SyntheticEvent } from "react";
import { useState } from "react";
import { hit_api } from "../utils";
import Input from "../components/input";
import Router from "next/router";
import Link from "next/link";


const Signup: NextPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = async (e: SyntheticEvent) => {
    e.preventDefault();
    console.log("submit", email, password);
    let { data } = await hit_api(
      "http://localhost:8000/auth/api/client/create/",
      "POST",
      { email, password }
    ); 
    console.log("data", data);
    if (data.success) {
      Router.push("/");
    }
  };

  return (
    <div className="flex flex-col gap-8 ml-8 mt-16">
      <h1>Signup</h1>
      <form className="flex flex-col gap-2 w-80" onSubmit={handleSubmit}>
        <Input
          type="email"
          name="email"
          value={email}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setEmail(e.target.value)
          }
        />
        <Input
          type="password"
          name="password"
          value={password}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setPassword(e.target.value)
          }
        />
        <Input
          type="password"
          name="confirm-password"
          value={confirmPassword}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setConfirmPassword(e.target.value)
          }
        />
        <button type="submit" className="bg-blue-500 rounded-lg p-2 w-32">
          Create account
        </button>
        <Link href="/login">already signed up? go to login page</Link>
      </form>
    </div>
  );
};

export default Signup;

// TODO:
// next_url
// redirection
// forgot_password thing
