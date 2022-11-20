import json

from aiohttp import ClientSession
from xbox.webapi.authentication.manager import AuthenticationManager


class SpartanTokenProof:
    def __init__(self):
        self.Token: str = ""
        self.TokenType: str = ""


class SpartanTokenRequest:
    def __init__(self):
        self.Audience: str = ""
        self.MinVersion: str = ""
        self.Proof: SpartanTokenProof = None


class HaloAuthenticationClient:
    def __init__(self):
        self.HEADERS_CQS = {
            "User-Agent": "HaloWaypoint/2021112313511900 CFNetwork/1327.0.4 Darwin/21.2.0",
            "Accept": "application/json",
        }
    async def async_GetSpartanToken(self, xstsToken: str):
        async with ClientSession() as session:
            tokenRequest = SpartanTokenRequest()
            tokenRequest.Audience = "urn:343:s3:services"
            tokenRequest.MinVersion = "4"
            tokenRequest.Proof = SpartanTokenProof()
            tokenRequest.Proof.Token = xstsToken
            tokenRequest.Proof.TokenType = "Xbox_XSTSv3"
            # Refresh tokens if we have them
            params = json.dumps(tokenRequest.__dict__, default=lambda o: o.__dict__)

            params = dict(tokenRequest.__dict__)
            params['Proof'] = {
                'Token': tokenRequest.Proof.Token,
                'TokenType': tokenRequest.Proof.TokenType
            }
            """
            M.R3_SN1.16c13941-f8f1-c770-27de-432f6e9c416c
            """
            resp = await session.post(
                'https://settings.svc.halowaypoint.com/spartan-token', data=params, headers=self.HEADERS_CQS
            )

            debug = True
