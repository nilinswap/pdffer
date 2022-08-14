// Next.js API route support: https://nextjs.org/docs/api-routes/introduction


import supertokens from 'supertokens-node';
import { superTokensNextWrapper } from 'supertokens-node/nextjs';
import { verifySession } from 'supertokens-node/recipe/session/framework/express';
import { backendConfig } from '../../config/backendConfig';

supertokens.init(backendConfig())

export default async function handler(req, res) {
  await superTokensNextWrapper(
    async (next) => {
      return await verifySession()(req, res, next)
    },
    req,
    res
  )

  return res.status(200).json({ name: 'John Doe' })
}