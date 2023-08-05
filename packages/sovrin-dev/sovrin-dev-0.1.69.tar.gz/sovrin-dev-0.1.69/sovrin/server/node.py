import json
from _sha256 import sha256
from copy import deepcopy
from operator import itemgetter
from typing import Iterable

import pyorient
from ledger.compact_merkle_tree import CompactMerkleTree
from ledger.ledger import Ledger
from ledger.serializers.compact_serializer import CompactSerializer

from ledger.util import F
from plenum.common.exceptions import InvalidClientRequest, \
    UnauthorizedClientRequest
from plenum.common.txn import RAW, ENC, HASH, NAME, VERSION
from plenum.common.types import Reply, Request, RequestAck, RequestNack, f, \
    NODE_PRIMARY_STORAGE_SUFFIX
from plenum.common.util import getlogger, error
from plenum.persistence.storage import initStorage
from plenum.server.node import Node as PlenumNode
from sovrin.common.txn import TXN_TYPE, \
    TARGET_NYM, allOpKeys, validTxnTypes, ATTRIB, SPONSOR, NYM,\
    ROLE, STEWARD, USER, GET_ATTR, DISCLO, DATA, GET_NYM, \
    TXN_ID, TXN_TIME, reqOpKeys, GET_TXNS, LAST_TXN, TXNS, \
    getTxnOrderedFields, CRED_DEF, GET_CRED_DEF, isValidRole
from sovrin.common.util import getConfig, dateTimeEncoding
from sovrin.persistence.identity_graph import IdentityGraph
from sovrin.persistence.secondary_storage import SecondaryStorage
from sovrin.server.client_authn import TxnBasedAuthNr

logger = getlogger()


class Node(PlenumNode):
    def __init__(self,
                 name,
                 nodeRegistry,
                 clientAuthNr=None,
                 ha=None,
                 cliname=None,
                 cliha=None,
                 basedirpath=None,
                 primaryDecider=None,
                 pluginPaths: Iterable[str] = None,
                 storage=None,
                 config=None):
        self.config = config or getConfig()
        self.graphStorage = self.getGraphStorage(name)
        super().__init__(name=name,
                         nodeRegistry=nodeRegistry,
                         clientAuthNr=clientAuthNr,
                         ha=ha,
                         cliname=cliname,
                         cliha=cliha,
                         basedirpath=basedirpath,
                         primaryDecider=primaryDecider,
                         pluginPaths=pluginPaths,
                         storage=storage,
                         config=self.config)
        self._addTxnsToGraphIfNeeded()

    def getSecondaryStorage(self):
        return SecondaryStorage(self.graphStorage, self.primaryStorage)

    def getGraphStorage(self, name):
        return IdentityGraph(self._getOrientDbStore(name,
                                                    pyorient.DB_TYPE_GRAPH))

    def getPrimaryStorage(self):
        """
        This is usually an implementation of Ledger
        """
        if self.config.primaryStorage is None:
            fields = getTxnOrderedFields()
            return Ledger(CompactMerkleTree(hashStore=self.hashStore),
                          dataDir=self.dataLocation,
                          serializer=CompactSerializer(fields=fields),
                          fileName=self.config.domainTransactionsFile)
        else:
            return initStorage(self.config.primaryStorage,
                               name=self.name + NODE_PRIMARY_STORAGE_SUFFIX,
                               dataDir=self.dataLocation,
                               config=self.config)

    def _addTxnsToGraphIfNeeded(self):
        i = 0
        txnCountInGraph = self.graphStorage.countTxns()
        for seqNo, txn in self.domainLedger.getAllTxn().items():
            if seqNo > txnCountInGraph:
                txn[F.seqNo.name] = seqNo
                self.storeTxnInGraph(txn)
                i += 1
        logger.debug("{} adding {} transactions to graph from ledger".
                     format(self, i))
        return i

    def checkValidOperation(self, identifier, reqId, msg):
        self.checkValidSovrinOperation(identifier, reqId, msg)
        super().checkValidOperation(identifier, reqId, msg)

    def checkValidSovrinOperation(self, identifier, reqId, msg):
        unknownKeys = set(msg.keys()).difference(set(allOpKeys))
        if unknownKeys:
            raise InvalidClientRequest(identifier, reqId,
                                       'invalid keys "{}"'.
                                       format(",".join(unknownKeys)))

        missingKeys = set(reqOpKeys).difference(set(msg.keys()))
        if missingKeys:
            raise InvalidClientRequest(identifier, reqId,
                                       'missing required keys "{}"'.
                                       format(",".join(missingKeys)))

        if msg[TXN_TYPE] not in validTxnTypes:
            raise InvalidClientRequest(identifier, reqId, 'invalid {}: {}'.
                                       format(TXN_TYPE, msg[TXN_TYPE]))

        if msg[TXN_TYPE] == ATTRIB:
            dataKeys = {RAW, ENC, HASH}.intersection(set(msg.keys()))
            if len(dataKeys) != 1:
                raise InvalidClientRequest(identifier, reqId,
                                           '{} should have one and only one of '
                                           '{}, {}, {}'
                                           .format(ATTRIB, RAW, ENC, HASH))

            if not (not msg.get(TARGET_NYM) or
                        self.graphStorage.hasNym(msg[TARGET_NYM])):
                raise InvalidClientRequest(identifier, reqId,
                                           '{} should be added before adding '
                                           'attribute for it'.
                                           format(TARGET_NYM))

        if msg[TXN_TYPE] == NYM:
            role = msg.get(ROLE) or USER
            if not isValidRole(role):
                raise InvalidClientRequest(identifier, reqId,
                                           "{} not a valid role".
                                           format(role))
            if self.graphStorage.hasNym(msg[TARGET_NYM]):
                raise InvalidClientRequest(identifier, reqId,
                                           "{} is already present".
                                           format(msg[TARGET_NYM]))

    authorizedAdders = {
        STEWARD: (STEWARD,),
        SPONSOR: (STEWARD,),
        USER: (STEWARD, SPONSOR),
    }

    def checkRequestAuthorized(self, request: Request):
        op = request.operation
        typ = op[TXN_TYPE]

        s = self.graphStorage  # type: IdentityGraph

        origin = request.identifier
        originRole = s.getRole(origin)

        if typ == NYM:
            role = op.get(ROLE) or USER
            authorizedAdder = self.authorizedAdders[role]
            if originRole not in authorizedAdder:
                raise UnauthorizedClientRequest(
                    request.identifier,
                    request.reqId,
                    "{} cannot add {}".format(originRole, role))
        elif typ == ATTRIB:
            if op.get(TARGET_NYM) and not \
                            s.getSponsorFor(op[TARGET_NYM]) == origin:
                raise UnauthorizedClientRequest(
                        request.identifier,
                        request.reqId,
                        "Only user's sponsor can add attribute for that user")
        # TODO: Just for now. Later do something meaningful here
        elif typ in [DISCLO, GET_ATTR, CRED_DEF, GET_CRED_DEF]:
            pass
        else:
            return super().checkRequestAuthorized(request)

    def defaultAuthNr(self):
        return TxnBasedAuthNr(self.graphStorage)

    def processRequest(self, request: Request, frm: str):
        if request.operation[TXN_TYPE] == GET_NYM:
            self.transmitToClient(RequestAck(request.reqId), frm)
            nym = request.operation[TARGET_NYM]
            txn = self.graphStorage.getAddNymTxn(nym)
            txnId = self.genTxnId(request.identifier, request.reqId)
            result = {f.IDENTIFIER.nm: request.identifier,
                      f.REQ_ID.nm: request.reqId,
                      DATA: json.dumps(txn) if txn else None,
                      TXN_ID: txnId
                      }
            result.update(request.operation)
            self.transmitToClient(Reply(result), frm)
        elif request.operation[TXN_TYPE] == GET_TXNS:
            nym = request.operation[TARGET_NYM]
            origin = request.identifier
            if nym != origin:
                msg = "You can only receive transactions for yourself"
                self.transmitToClient(RequestNack(request.reqId, msg), frm)
            else:
                self.transmitToClient(RequestAck(request.reqId), frm)
                data = request.operation.get(DATA)
                addNymTxn = self.graphStorage.getAddNymTxn(origin)
                txnIds = [addNymTxn[TXN_ID], ] + self.graphStorage.\
                    getAddAttributeTxnIds(origin)
                # If sending transactions to a user then should send user's
                # sponsor creation transaction also
                if addNymTxn.get(ROLE) == USER:
                    sponsorNymTxn = self.graphStorage.getAddNymTxn(
                        addNymTxn.get(f.IDENTIFIER.nm))
                    txnIds = [sponsorNymTxn[TXN_ID], ] + txnIds
                # TODO: Remove this log statement
                logger.debug("{} getting replies for {}".format(self, txnIds))
                result = self.secondaryStorage.getReplies(*txnIds, seqNo=data)
                txns = sorted(list(result.values()), key=itemgetter(F.seqNo.name))
                lastTxn = str(txns[-1][F.seqNo.name]) if len(txns) > 0 else data
                result = {
                    TXN_ID: self.genTxnId(
                        request.identifier, request.reqId)
                }
                result.update(request.operation)
                result[DATA] = json.dumps({
                    LAST_TXN: lastTxn,
                    TXNS: txns
                }, default=dateTimeEncoding)
                result.update({
                    f.IDENTIFIER.nm: request.identifier,
                    f.REQ_ID.nm: request.reqId,
                })
                self.transmitToClient(Reply(result), frm)
        elif request.operation[TXN_TYPE] == GET_CRED_DEF:
            issuerNym = request.operation[TARGET_NYM]
            name = request.operation[DATA][NAME]
            version = request.operation[DATA][VERSION]
            credDef = self.graphStorage.getCredDef(issuerNym, name, version)
            result = {
                TXN_ID: self.genTxnId(
                    request.identifier, request.reqId)
            }
            result.update(request.operation)
            result[DATA] = json.dumps(credDef)
            result.update({
                f.IDENTIFIER.nm: request.identifier,
                f.REQ_ID.nm: request.reqId,
            })
            self.transmitToClient(Reply(result), frm)
        else:
            super().processRequest(request, frm)

    def storeTxnAndSendToClient(self, reply):
        """
        Does 4 things in following order
         1. Add reply to ledger.
         2. Send the reply to client.
         3. Add the reply to identity graph if needed.
         4. Add the reply to storage so it can be served later if the
         client requests it.
        """
        txnWithMerkleInfo = self.storeTxnInLedger(reply.result)
        self.sendReplyToClient(Reply(txnWithMerkleInfo))
        self.storeTxnInGraph(txnWithMerkleInfo)

    def storeTxnInLedger(self, result):
        if result[TXN_TYPE] == ATTRIB:
            # Creating copy of result so that `RAW`, `ENC` or `HASH` can be
            # replaced by their hashes. We do not insert actual attribute data
            # in the ledger but only the hash of it.
            result = deepcopy(result)
            if RAW in result:
                result[RAW] = sha256(result[RAW].encode()).hexdigest()
            elif ENC in result:
                result[ENC] = sha256(result[ENC].encode()).hexdigest()
            elif HASH in result:
                result[HASH] = result[HASH]
            else:
                error("Transaction missing required field")
            merkleInfo = self.addToLedger(result)
        else:
            merkleInfo = self.addToLedger(result)
        result.update(merkleInfo)
        return result

    def storeTxnInGraph(self, result):
        result = deepcopy(result)
        # Remove root hash and audit path from result if present since they can
        # be generated on the fly from the ledger so no need to store it
        result.pop(F.rootHash.name, None)
        result.pop(F.auditPath.name, None)

        if result[TXN_TYPE] == NYM:
            self.graphStorage.addNymTxnToGraph(result)
        elif result[TXN_TYPE] == ATTRIB:
            self.graphStorage.addAttribTxnToGraph(result)
        elif result[TXN_TYPE] == CRED_DEF:
            self.graphStorage.addCredDefTxnToGraph(result)

    def sendReplyToClient(self, reply):
        identifier = reply.result.get(f.IDENTIFIER.nm)
        # In case of genesis transactions when no identifier is present
        if identifier in self.clientIdentifiers:
            self.transmitToClient(reply, self.clientIdentifiers[identifier])
        else:
            logger.debug("Could not find identifier {} to send reply".
                         format(identifier))

    def addToLedger(self, txn):
        merkleInfo = self.primaryStorage.append(txn)
        return merkleInfo

    def getReplyFor(self, request):
        result = self.secondaryStorage.getReply(request.identifier,
                                                request.reqId,
                                                type=request.operation[TXN_TYPE])
        return Reply(result) if result else None

    def doCustomAction(self, ppTime: float, req: Request) -> None:
        """
        Execute the REQUEST sent to this Node

        :param ppTime: the time at which PRE-PREPARE was sent
        :param req: the client REQUEST
        """
        if req.operation[TXN_TYPE] == NYM and \
                self.graphStorage.hasNym(req.operation[TARGET_NYM]):
            reason = "nym {} is already added".format(req.operation[TARGET_NYM])
            if req.identifier in self.clientIdentifiers:
                self.transmitToClient(RequestNack(req.reqId, reason),
                                      self.clientIdentifiers[req.identifier])
        else:
            reply = self.generateReply(int(ppTime), req)
            self.storeTxnAndSendToClient(reply)

    def generateReply(self, ppTime: float, req: Request):
        operation = req.operation
        txnId = self.genTxnId(req.identifier, req.reqId)
        result = {TXN_ID: txnId, TXN_TIME: ppTime}
        # if operation[TXN_TYPE] == GET_ATTR:
        #     # TODO: Very inefficient, queries all transactions and looks for the
        #     # DISCLOSE for the clients and returns all. We probably change the
        #     # transaction schema or have some way to zero in on the DISCLOSE for
        #     # the attribute that is being looked for
        #     attrs = []
        #     for txn in self.primaryStorage.getAllTxn().values():
        #         if txn.get(TARGET_NYM, None) == req.identifier and txn[TXN_TYPE] == \
        #                 DISCLOSE:
        #             attrs.append({DATA: txn[DATA], NONCE: txn[NONCE]})
        #     if attrs:
        #         result[ATTRIBUTES] = attrs
        #
        result.update(operation)
        result.update({
            f.IDENTIFIER.nm: req.identifier,
            f.REQ_ID.nm: req.reqId,
        })

        return Reply(result)
