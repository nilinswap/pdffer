import dynamic from "next/dynamic";
import Head from "next/head";
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import Passwordless from "supertokens-auth-react/recipe/passwordless";
import supertokensNode from "supertokens-node";
import Session from "supertokens-node/recipe/session";

const PasswordlessAuthNoSSR = dynamic(
  new Promise((res) => res(Passwordless.PasswordlessAuth)),
  { ssr: false }
);

export default function Home(props) {
  return (
    <PasswordlessAuthNoSSR>
      <ProtectedPage />
    </PasswordlessAuthNoSSR>
  );
}

const ProtectedPage = ({ userId }) => {

  async function logoutClicked() {
    await Passwordless.signOut();
    Passwordless.redirectToAuth();
  }

  return (
    <div>
      <Head>
        <title>Pdffer</title>
        <meta name="description" content="create pdfs easily" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen p-4 flex flex-col flex-1 justify-center items-center">
        <div className="flex gap-4">
          <text className="text-2xl">api key</text>
          <div className="p-2 bg-slate-300 rounded-sm">
            ajsdfljasdfljasdfjlasdfjkladfjs
          </div>
        </div>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Pdffer @ 2022
          <span className={styles.logo}>
            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  );
};
