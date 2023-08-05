import inspect
import json
import shutil
from contextlib import ExitStack
from typing import Iterable, Union, Tuple

import pyorient

from sovrin.anon_creds.issuer import Issuer
from sovrin.anon_creds.prover import Prover
from sovrin.anon_creds.verifier import Verifier

from plenum.client.signer import SimpleSigner
from plenum.common.looper import Looper
from plenum.common.txn import REQACK, DATA
from plenum.common.types import HA
from plenum.common.util import getMaxFailures, runall, getlogger, getConfig
from plenum.persistence import orientdb_store
from plenum.persistence.orientdb_store import OrientDbStore
from plenum.test.eventually import eventually
from plenum.test.helper import TestNodeSet as PlenumTestNodeSet
from plenum.test.helper import checkNodesConnected, \
    checkNodesAreReady, checkSufficientRepliesRecvd, checkLastClientReqForNode,\
    buildCompletedTxnFromReply, TestStack, TestNodeCore, StackedTester
from plenum.test.helper import genTestClient as genPlenumTestClient
from plenum.test.helper import genTestClientProvider as \
    genPlenumTestClientProvider
from plenum.test.testable import Spyable
from sovrin.client.anoncreds_role import AnonCredsRole
from sovrin.client.client import Client
from sovrin.client.client_storage import ClientStorage
from sovrin.client.wallet import Wallet
from sovrin.common.txn import ATTRIB, NYM, TARGET_NYM, TXN_TYPE, ROLE, \
    TXN_ID, USER
from sovrin.server.node import Node

logger = getlogger()


class Scenario(ExitStack):
    """
    Test context
    simple container to toss in a dynamic context to streamline testing
    """

    def __init__(self,
                 nodeCount=None,
                 nodeRegistry=None,
                 nodeSet=None,
                 looper=None,
                 tmpdir=None):
        super().__init__()

        self.actor = None  # type: Organization

        if nodeSet is None:
            self.nodes = self.enter_context(TestNodeSet(count=nodeCount,
                                                        nodeReg=nodeRegistry,
                                                        tmpdir=tmpdir))
        else:
            self.nodes = nodeSet
        self.nodeReg = self.nodes.nodeReg
        if looper is None:
            self.looper = self.enter_context(Looper(self.nodes))
        else:
            self.looper = looper
        self.tmpdir = tmpdir
        self.ran = []  # history of what has been run
        self.userId = None
        self.userNym = None
        self.sponsor = None
        self.sponsorNym = None
        self.agent = None
        self.agentNym = None

    def run(self, *coros):
        new = []
        for c in coros:
            if inspect.isfunction(c) or inspect.ismethod(c):
                new.append(c(self))  # call it with this context
            else:
                new.append(c)
        if new:
            result = self.looper.run(*new)
            self.ran.extend(coros)
            return result

    def ensureRun(self, *coros):
        """
        Ensures the coro gets run, in other words, this method optionally
        runs the coro if it has not already been run in this scenario
        :param coros:
        :return:
        """
        unrun = [c for c in coros if c not in self.ran]
        return self.run(*unrun)

    async def start(self):
        await checkNodesConnected(self.nodes)
        await eventually(checkNodesAreReady,
                         self.nodes,
                         retryWait=.25,
                         timeout=20,
                         ratchetSteps=10)

    async def startClient(self, org=None):
        org = org if org else self.actor
        self.looper.add(org.client)
        await org.client.ensureConnectedToNodes()

    def copyOfInBox(self, org=None):
        org = org if org else self.actor
        return org.client.inBox.copy()

    async def checkAcks(self, org=None, count=1, minusInBox=None):
        org = org if org else self.actor
        ib = self.copyOfInBox(org)
        if minusInBox:
            for x in minusInBox:
                ib.remove(x)

        for node in self.nodes:
            await eventually(self.checkInboxForReAck,
                             org.client.name,
                             ib,
                             REQACK,
                             node,
                             count,
                             retryWait=.1,
                             timeout=10,
                             ratchetSteps=10)

    @staticmethod
    def checkInboxForReAck(clientName, clientInBox, op, fromNode,
                           expectedCount: int):
        msg = 'Got your request client ' + clientName
        actualCount = sum(
            1 for x in clientInBox
            if x[0]['op'] == op and x[1] == fromNode.clientstack.name)
        assert actualCount == expectedCount

    async def checkReplies(self,
                           reqs,
                           org=None,
                           retryWait=.25,
                           timeout=None,
                           ratchetSteps=10):
        org = org if org else self.actor
        if not isinstance(reqs, Iterable):
            reqs = [reqs]

        if timeout is None:
            timeout = len(reqs) * 5 + 5

        nodeCount = sum(1 for _ in self.nodes)
        f = getMaxFailures(nodeCount)
        corogen = (eventually(checkSufficientRepliesRecvd,
                              org.client.inBox,
                              r.reqId,
                              f,
                              retryWait=retryWait,
                              timeout=timeout,
                              ratchetSteps=ratchetSteps) for r in reqs)

        return await runall(corogen)

    async def send(self, op, org=None):
        org = org if org else self.actor
        req = org.client.submit(op)[0]
        for node in self.nodes:
            await eventually(checkLastClientReqForNode,
                             node,
                             req,
                             retryWait=1,
                             timeout=10)
        return req

    async def sendAndCheckAcks(self, op, count: int=1, org=None):
        baseline = self.copyOfInBox()  # baseline of client inBox so we can net it out
        req = await self.send(op, org)
        await self.checkAcks(count=count, minusInBox=baseline)
        return req

    def genOrg(self):
        cli = genTestClientProvider(nodes=self.nodes,
                                    nodeReg=self.nodeReg.extractCliNodeReg(),
                                    tmpdir=self.tmpdir)
        return Organization(cli)

    def addAgent(self):
        self.agent = self.genOrg()
        return self.agent

    def addSponsor(self):
        self.sponsor = self.genOrg()
        return self.sponsor


class Organization:
    def __init__(self, client=None):
        self.client = client
        self.wallet = Wallet(self.client)  # created only once per organization
        self.userWallets = {}  # type: Dict[str, Wallet]

    # @property
    # def client(self):
    #     if self._client is None:
    #         self._client = genTestClient(nodeReg=self.s.nodeReg.extractCliNodeReg(), tmpdir=self.s.tmpdir)
    #         self.s.looper.addNextable(self._client)
    #     return self._client

    # def createUserWallet(self, userId: str):
    #     self.userWallets[userId] = UserWallet(self.client)

    def removeUserWallet(self, userId: str):
        if userId in self.userWallets:
            del self.userWallets[userId]
        else:
            raise ValueError("No wallet exists for this user id")

    # def getUserWallet(self, userId: str) -> UserWallet:
    #     if userId in self.userWallets:
    #         return self.userWallets[userId]
    #     else:
    #         raise ValueError("No wallet exists for this user id")

    def addTxnsForCompletedRequestsInWallet(self, reqs: Iterable, wallet:
                                            Wallet):
        for req in reqs:
            reply, status = self.client.getReply(req.reqId)
            if status == "CONFIRMED":
                # TODO Figure out the actual implementation of
                # TODO     `buildCompletedTxnFromReply`. This is just a stub
                # TODO     implementation
                txn = buildCompletedTxnFromReply(req, reply)
                # TODO Move this logic in wallet
                if txn['txnType'] == ATTRIB and txn['data'] is not None:
                    attr = list(txn['data'].keys())[0]
                    if attr in wallet.attributeEncKeys:
                        key = wallet.attributeEncKeys.pop(attr)
                        txn['secretKey'] = key
                wallet.addCompletedTxn(txn)


class TempStorage:

    def cleanupDataLocation(self):
        loc = self.dataLocation
        try:
            shutil.rmtree(loc)
        except Exception as ex:
            logger.debug("Error while removing temporary directory {}".format(
                ex))
        try:
            self.store.client.db_drop(self.name)
            logger.debug("Dropped db {}".format(self.name))
        except Exception as ex:
            logger.debug("Error while dropping db {}: {}".format(self.name,
                                                                 ex))


# noinspection PyShadowingNames,PyShadowingNames
@Spyable(
    methods=[Node.handleOneNodeMsg, Node.processRequest, Node.processOrdered,
             Node.postToClientInBox, Node.postToNodeInBox, "eatTestMsg",
             Node.decidePrimaries, Node.startViewChange, Node.discard,
             Node.reportSuspiciousNode, Node.reportSuspiciousClient,
             Node.processRequest, Node.processPropagate, Node.propagate,
             Node.forward, Node.send, Node.processInstanceChange,
             Node.checkPerformance])
class TestNode(TempStorage, TestNodeCore, Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        TestNodeCore.__init__(self, *args, **kwargs)

    def _getOrientDbStore(self, name, dbType):
        if not hasattr(self, '_orientDbStore'):
            self._orientDbStore = orientdb_store.createOrientDbInMemStore(
                self.config, name, dbType)
        return self._orientDbStore

    def onStopping(self, *args, **kwargs):
        self.cleanupDataLocation()
        try:
            self.graphStorage.client.db_drop(self.name)
            logger.debug("Dropped db {}".format(self.name))
        except Exception as ex:
            logger.debug("Error while dropping db {}: {}".format(self.name,
                                                                 ex))
        # config = getConfig()
        # os.system(config.OrientDB['shutdownScript'])
        super().onStopping(*args, **kwargs)


class TestNodeSet(PlenumTestNodeSet):
    def __init__(self,
                 names: Iterable[str]=None,
                 count: int=None,
                 nodeReg=None,
                 tmpdir=None,
                 keyshare=True,
                 primaryDecider=None,
                 pluginPaths: Iterable[str]=None,
                 testNodeClass=TestNode):
        super().__init__(names, count, nodeReg, tmpdir, keyshare,
                         primaryDecider=primaryDecider,
                         pluginPaths=pluginPaths,
                         testNodeClass=testNodeClass)


class TestClientStorage(TempStorage, ClientStorage):
    def __init__(self, name, baseDir):
        config = getConfig()
        store = OrientDbStore(user=config.OrientDB["user"],
                              password=config.OrientDB["password"],
                              dbName=name,
                              storageType=pyorient.STORAGE_TYPE_MEMORY)
        ClientStorage.__init__(self, name, baseDir, store)
        TempStorage.__init__(self)


@Spyable(methods=[Client.handleOneNodeMsg, Client.requestPendingTxns])
class TestClient(Client, StackedTester):
    @staticmethod
    def stackType():
        return TestStack

    def getStorage(self, baseDirPath=None):
        return TestClientStorage(self.name, baseDirPath)

    def onStopping(self, *args, **kwargs):
        self.storage.cleanupDataLocation()
        # # TODO: find a better way to clear wallet
        # try:
        #     shutil.rmtree(self.wallet.storage.dataLocation)
        # except Exception as ex:
        #     logger.debug("Exception while deleting {}'s wallet {}"
        #                  .format(self, ex))
        super().onStopping(*args, **kwargs)


class TestAnonCredsRole(AnonCredsRole):
    @property
    def sovrinClientClass(self):
        return TestClient


class TestIssuer(TestAnonCredsRole, Issuer):
    pass


class TestProver(TestAnonCredsRole, Prover):
    pass


class TestVerifier(TestAnonCredsRole, Verifier):
    pass


def genTestClient(nodes: TestNodeSet=None,
                  nodeReg=None,
                  tmpdir=None,
                  signer=None,
                  peerHA: Union[HA, Tuple[str, int]]=None,
                  testClientClass=TestClient,
                  usePoolLedger=False) -> TestClient:
    testClient = genPlenumTestClient(nodes,
                               nodeReg,
                               tmpdir,
                               signer,
                               testClientClass,
                               bootstrapKeys=False,
                               usePoolLedger=usePoolLedger)
    testClient.peerHA = peerHA
    return testClient


def genConnectedTestClient(looper,
                           nodes: TestNodeSet=None,
                           nodeReg=None,
                           tmpdir=None,
                           signer=None) -> TestClient:
    c = genTestClient(nodes, nodeReg=nodeReg, tmpdir=tmpdir, signer=signer)
    looper.add(c)
    looper.run(c.ensureConnectedToNodes())
    return c


def genTestClientProvider(nodes: TestNodeSet=None,
                          nodeReg=None,
                          tmpdir=None,
                          clientGnr=genTestClient):
    return genPlenumTestClientProvider(nodes, nodeReg, tmpdir, clientGnr)


def clientFromSigner(signer, looper, nodeSet, tdir):
    s = genTestClient(nodeSet, signer=signer, tmpdir=tdir)
    looper.add(s)
    looper.run(s.ensureConnectedToNodes())
    return s


def createNym(looper, nym, creatorClient, creatorSigner, role):
    op = {
        TARGET_NYM: nym,
        TXN_TYPE: NYM,
        ROLE: role
    }
    return submitAndCheck(looper,
                          creatorClient,
                          op,
                          identifier=creatorSigner.identifier)[0]


def addUser(looper, creatorClient, creatorSigner, name):
    usigner = SimpleSigner()
    createNym(looper, usigner.verstr, creatorClient, creatorSigner, USER)
    return usigner


def submitAndCheck(looper, client, op, identifier):
    # TODO: This assumes every transaction will have an edge in graph, why?
    # Fix this
    txnsBefore = client.getTxnsByType(op[TXN_TYPE])
    client.submit(op, identifier=identifier)
    txnsAfter = []

    def checkTxnCountAdvanced():
        nonlocal txnsAfter
        txnsAfter = client.getTxnsByType(op[TXN_TYPE])
        logger.debug("old and new txns {} {}".format(txnsBefore, txnsAfter))
        assert len(txnsAfter) > len(txnsBefore)

    looper.run(eventually(checkTxnCountAdvanced, retryWait=1, timeout=15))
    txnIdsBefore = [txn[TXN_ID] for txn in txnsBefore]
    txnIdsAfter = [txn[TXN_ID] for txn in txnsAfter]
    logger.debug("old and new txnids {} {}".format(txnIdsBefore, txnIdsAfter))
    return list(set(txnIdsAfter) - set(txnIdsBefore))


def addNym(ha, looper, nym, sponsNym, sponsor):
    op = {
        TARGET_NYM: nym,
        TXN_TYPE: NYM,
        ROLE: USER,
        DATA: json.dumps({'ha': ha})
    }
    submitAndCheck(looper, sponsor, op, identifier=sponsNym)


class TestGraphStorage:
    def __init__(self):
        pass
