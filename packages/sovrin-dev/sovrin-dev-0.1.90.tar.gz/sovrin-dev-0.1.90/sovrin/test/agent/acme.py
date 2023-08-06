import os
import random

from plenum.common.txn import NAME, VERSION
from plenum.common.util import getlogger

from anoncreds.test.conftest import staticPrimes

from sovrin.agent.agent import WalletedAgent, runAgent
from sovrin.anon_creds.issuer import AttribType, AttribDef
from sovrin.client.client import Client
from sovrin.client.wallet.link import Link
from sovrin.client.wallet.wallet import Wallet
from sovrin.common.util import getConfig
import sovrin.test.random_data as randomData

logger = getlogger()


class AcmeAgent(WalletedAgent):
    def __init__(self,
                 basedirpath: str,
                 client: Client=None,
                 wallet: Wallet=None,
                 port: int=None):
        if not basedirpath:
            config = getConfig()
            basedirpath = basedirpath or os.path.expanduser(config.baseDir)

        super().__init__('Acme Corp', basedirpath, client, wallet, port)

        self._seqNos = {
            ("Job-Certificate", "0.1"): (None, None)
        }

        self._attributes = {
            "57fbf9dc8c8e6acde33de98c6d747b28c": {
                "employee_name": "Alice Garcia",
                "employee_status": "Permanent",
                "experience": "3 years",
                "salary_bracket": "between $50,000 to $100,000"
            },
            "3a2eb72eca8b404e8d412c5bf79f2640": {
                "employee_name": "Carol Atkinson",
                "employee_status": "Permanent",
                "experience": "2 years",
                "salary_bracket": "between $60,000 to $90,000"
            },
            "8513d1397e87cada4214e2a650f603eb": {
                "employee_name": "Frank Jeffrey",
                "employee_status": "Temporary",
                "experience": "4 years",
                "salary_bracket": "between $40,000 to $80,000"
            },
            "810b78be79f29fc81335abaa4ee1c5e8": {
                "employee_name": "Craig Richards",
                "employee_status": "On Contract",
                "experience": "3 years",
                "salary_bracket": "between $50,000 to $70,000"
            },
        }

    def addKeyIfNotAdded(self):
        wallet = self.wallet
        if not wallet.identifiers:
            wallet.addSigner(seed=b'Acme0000000000000000000000000000')

    def getAvailableClaimList(self):
        return []

    def getClaimList(self, claimNames=None):
        allClaims = [{
            "name": "Job-Certificate",
            "version": "0.1",
            "claimDefSeqNo": "<claimDefSeqNo>",
            "values": {
                "employee_name": "Alice Gracia",
                "employee_status": "Permanent",
                "experience": "3 years",
                "salary_bracket": "between $50,000 to $100,000"
            }
        }]
        return [c for c in allClaims if not claimNames or c[NAME] in claimNames]

    def addClaimDefsToWallet(self):
        name, version = "Job-Certificate", "0.1"
        credDefSeqNo, issuerKeySeqNo = self._seqNos[(name, version)]
        staticPrime = staticPrimes().get("prime1")
        attrNames = ["employee_name", "employee_status", "experience",
                     "salary_bracket"]
        super().addClaimDefsToWallet(name="Job Application",
                                     version="0.1",
                                     attrNames=attrNames,
                                     staticPrime=staticPrime,
                                     credDefSeqNo=credDefSeqNo,
                                     issuerKeySeqNo=issuerKeySeqNo)

    def getAttributes(self, nonce):
        attrs = self._attributes.get(nonce)
        if not attrs:
            attrs = {
                "employee_name": random.choice(randomData.NAMES),
                "employee_status": random.choice(randomData.EMPLOYEE_STATUS),
                "experience": random.choice(randomData.EXPERIENCE),
                "salary_bracket": random.choice(randomData.SALARY_BRACKET)
            }

        attribTypes = []
        for name in attrs:
            attribTypes.append(AttribType(name, encode=True))
        attribsDef = AttribDef("Job-Certificate", attribTypes)
        attribs = attribsDef.attribs(**attrs)
        return attribs

    def addLinksToWallet(self):
        wallet = self.wallet
        idr = wallet.defaultId
        for nonce, data in self._attributes.items():
            link = Link(data.get("name"), idr, nonce=nonce)
            wallet.addLinkInvitation(link)

    def bootstrap(self):
        self.addKeyIfNotAdded()
        self.addLinksToWallet()
        self.addClaimDefsToWallet()


def runAcme(name=None, wallet=None, basedirpath=None, port=None,
            startRunning=True, bootstrap=True):

    return runAgent(AcmeAgent, name or "Acme Corp", wallet, basedirpath,
             port, startRunning, bootstrap)

if __name__ == "__main__":
    runAcme(port=6666)
