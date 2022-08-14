import '../styles/globals.css'
import type { AppProps } from 'next/app'
import SuperTokensReact from "supertokens-auth-react";
import { frontendConfig } from "../config/frontendConfig";


if (typeof window !== "undefined") {
  // we only want to call this init function on the frontend, so
  // we check typeof window !== 'undefined'
  SuperTokensReact.init(frontendConfig());
}

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}

export default MyApp
