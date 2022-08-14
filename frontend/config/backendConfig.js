require("dotenv").config();

import Session from "supertokens-auth-react/recipe/session";
import PasswordlessNode from "supertokens-node/recipe/passwordless";
import SessionNode from "supertokens-node/recipe/session";
import { appInfo } from "./appInfo";
let { getEmailBody } = require("../utils/mailer");
// import { getEmailBody } from "../utils/mailer"
// console.log("getEmailBody", getEmailBody);
// function getEmailBody(a, b, c, d, e) {
//   // console.log(a, b, c, d, e);

//   return `
//     <html>
//     <body>
//       Hello World
//     </body>
//     </html>  
//   `
// }

export const backendConfig = () => {
  const nodemailer = require('nodemailer');

  const mailTransporter = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 465,
    secure: true,
    auth: {
        user: process.env.NEXT_PUBLIC_NODEMAILER_USER,
        pass: process.env.NEXT_PUBLIC_NODEMAILER_PASSWORD,
    },
  });

  return {
    framework: "express",
    supertokens: {
      connectionURI: "https://try.supertokens.com",
      // apiKey: "IF YOU HAVE AN API KEY FOR THE CORE, ADD IT HERE",
    },
    appInfo,
    recipeList: [
      PasswordlessNode.init({
        flowType: "USER_INPUT_CODE_AND_MAGIC_LINK",
        contactMethod: "EMAIL_OR_PHONE",
        createAndSendCustomEmail: async (input, context) => {
            try {
              console.log("getEmailBody", getEmailBody);
            let htmlBody = getEmailBody(
              appInfo.appName,
              Math.ceil(input.codeLifetime / 1000),
              input.urlWithLinkCode,
              input.userInputCode,
              input.email
            );
            await mailTransporter.sendMail({
              html: htmlBody,
              to: input.email,
              from: `Team Supertokens <${appInfo.appName}>`,
              sender: process.env.NEXT_PUBLIC_NODEMAILER_USER,
              subject: `Login to ${appInfo.appName}`,
            });
          } catch (err) {
            console.log(err);
          }
        },
        createAndSendCustomTextMessage: async (input, context) => {
          // Creating a Twilio account and set it up.
        },
      }),
      SessionNode.init(),
    ],
    isInServerlessEnv: true,
  };
};
