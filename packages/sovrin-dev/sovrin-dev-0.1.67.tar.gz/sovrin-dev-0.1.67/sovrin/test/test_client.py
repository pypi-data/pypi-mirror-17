import json

import base58
import libnacl.public
import pytest

from plenum.client.signer import SimpleSigner
from plenum.common.txn import REQNACK, ENC, RAW
from plenum.common.types import f, OP_FIELD_NAME
from plenum.common.util import adict, getlogger
from plenum.test.eventually import eventually

from sovrin.common.txn import ATTRIB, NYM, \
    TARGET_NYM, TXN_TYPE, ROLE, SPONSOR, ORIGIN, USER, \
    TXN_ID, NONCE, SKEY, REFERENCE
from sovrin.common.util import getSymmetricallyEncryptedVal
from sovrin.test.helper import genTestClient, createNym, submitAndCheck

logger = getlogger()


# TODO use wallet instead of SimpleSigner in client


def checkNacks(client, reqId, contains='', nodeCount=4):
    reqs = [x for x, _ in client.inBox if x[OP_FIELD_NAME] == REQNACK and
            x[f.REQ_ID.nm] == reqId]
    for r in reqs:
        assert f.REASON.nm in r
        assert contains in r[f.REASON.nm]
    assert len(reqs) == nodeCount


# TODO Ordering of parameters is bad
def submitAndCheckNacks(looper, client, op, identifier,
                        contains='UnauthorizedClientRequest'):
    client.submit(op, identifier=identifier)
    looper.run(eventually(checkNacks,
                          client,
                          client.lastReqId,
                          contains, retryWait=1, timeout=15))


@pytest.fixture(scope="module")
def attributeData():
    return json.dumps({'name': 'Mario'})


@pytest.fixture(scope="module")
def addedRawAttribute(userSignerA, sponsor, sponsorSigner, attributeData,
                      looper):
    op = {
        ORIGIN: sponsorSigner.verstr,
        TARGET_NYM: userSignerA.verstr,
        TXN_TYPE: ATTRIB,
        RAW: attributeData
    }

    submitAndCheck(looper, sponsor, op, identifier=sponsorSigner.verstr)


@pytest.fixture(scope="module")
def symEncData(attributeData):
    encData, secretKey = getSymmetricallyEncryptedVal(attributeData)
    return adict(data=attributeData, encData=encData, secretKey=secretKey)


@pytest.fixture(scope="module")
def addedEncryptedAttribute(userSignerA, sponsor, sponsorSigner, looper,
                            symEncData):
    sponsorNym = sponsorSigner.verstr
    op = {
        TARGET_NYM: userSignerA.verstr,
        TXN_TYPE: ATTRIB,
        ENC: symEncData.encData
    }

    return submitAndCheck(looper, sponsor, op, identifier=sponsorNym)[0]


@pytest.fixture(scope="module")
def nonSponsor(looper, nodeSet, tdir):
    sseed = b'this is a secret sponsor seed...'
    sponsorSigner = SimpleSigner(seed=sseed)
    c = genTestClient(nodeSet, tmpdir=tdir, signer=sponsorSigner)
    for node in nodeSet:
        node.whitelistClient(c.name)
    looper.add(c)
    looper.run(c.ensureConnectedToNodes())
    return c


@pytest.fixture(scope="module")
def anotherSponsor(genned, steward, stewardSigner, tdir, looper):
    sseed = b'this is 1 secret sponsor seed...'
    signer = SimpleSigner(seed=sseed)
    c = genTestClient(genned, tmpdir=tdir, signer=signer)
    for node in genned:
        node.whitelistClient(c.name)
    looper.add(c)
    looper.run(c.ensureConnectedToNodes())
    createNym(looper, signer.verstr, steward, stewardSigner, SPONSOR)
    return c


def testNonStewardCannotCreateASponsor(genned, client1, client1Signer, looper):
    seed = b'this is a secret sponsor seed...'
    sponsorSigner = SimpleSigner(seed)

    sponsorNym = sponsorSigner.verstr

    op = {
        TARGET_NYM: sponsorNym,
        TXN_TYPE: NYM,
        ROLE: SPONSOR
    }

    submitAndCheckNacks(looper=looper, client=client1, op=op,
                        identifier=client1Signer.identifier,
                        contains="InvalidIdentifier")


def testStewardCreatesASponsor(updatedSteward, addedSponsor):
    pass


@pytest.mark.skipif(True, reason="Cannot create another sponsor with same nym")
def testStewardCreatesAnotherSponsor(genned, steward, stewardSigner, looper,
                                     sponsorSigner):
    createNym(looper, sponsorSigner.verstr, steward, stewardSigner, SPONSOR)
    return sponsorSigner


def testNonSponsorCannotCreateAUser(genned, looper, nonSponsor):

    sponsNym = nonSponsor.getSigner().verstr

    useed = b'this is a secret apricot seed...'
    userSigner = SimpleSigner(seed=useed)

    userNym = userSigner.verstr

    op = {
        TARGET_NYM: userNym,
        TXN_TYPE: NYM,
        ROLE: USER
    }

    submitAndCheckNacks(looper, nonSponsor, op, identifier=sponsNym,
                        contains="InvalidIdentifier")


def testSponsorCreatesAUser(updatedSteward, userSignerA):
    pass


@pytest.fixture(scope="module")
def nymsAddedInQuickSuccession(genned, addedSponsor, looper,
                               sponsor):
    usigner = SimpleSigner()
    opA = {
        TARGET_NYM: usigner.verstr,
        TXN_TYPE: NYM,
        ROLE: USER
    }
    opB = opA
    sponsorNym = sponsor.getSigner().verstr
    sponsor.submit(opA, opB, identifier=sponsorNym)
    try:
        submitAndCheck(looper, sponsor, opA, identifier=sponsorNym)
        submitAndCheckNacks(looper, sponsor, opB, identifier=sponsorNym)
    except Exception as ex:
        pass

    count = 0
    for name, node in genned.nodes.items():
        txns = node.domainLedger.getAllTxn()
        for seq, txn in txns.items():
            if txn[TXN_TYPE] == NYM and txn[TARGET_NYM] == usigner.verstr:
                count += 1

    assert(count == len(genned.nodes))


def testAddNymsInQuickSuccession(nymsAddedInQuickSuccession):
    pass


def testSponsorAddsAttributeForUser(addedRawAttribute):
    pass


def testSponsorAddsAliasForUser(addedSponsor, looper, sponsor, sponsorSigner):
    userSigner = SimpleSigner()
    txnId = createNym(looper, userSigner.verstr, sponsor, sponsorSigner, USER)

    sponsNym = sponsorSigner.verstr

    op = {
        TARGET_NYM: "jasonlaw",
        TXN_TYPE: NYM,
        # TODO: Should REFERENCE be symmetrically encrypted and the key
        # should then be disclosed in another transaction
        REFERENCE: txnId,
        ROLE: USER
    }

    submitAndCheck(looper, sponsor, op, identifier=sponsNym)


def testNonSponsorCannotAddAttributeForUser(nonSponsor, userSignerA, looper,
                                            genned, attributeData):

    nym = nonSponsor.getSigner().verstr

    op = {
        TARGET_NYM: userSignerA.verstr,
        TXN_TYPE: ATTRIB,
        RAW: attributeData
    }

    submitAndCheckNacks(looper, nonSponsor, op, identifier=nym,
                        contains="InvalidIdentifier")


def testOnlyUsersSponsorCanAddAttribute(userSignerA, looper, genned,
                                        steward, stewardSigner,
                                        attributeData, anotherSponsor):
    op = {
        TARGET_NYM: userSignerA.verstr,
        TXN_TYPE: ATTRIB,
        RAW: attributeData
    }

    submitAndCheckNacks(looper, anotherSponsor, op,
                        identifier=anotherSponsor.getSigner().verstr)


def testStewardCannotAddUsersAttribute(userSignerA, genned, looper, steward,
                                       stewardSigner, attributeData):
    op = {
        TARGET_NYM: userSignerA.verstr,
        TXN_TYPE: ATTRIB,
        RAW: attributeData
    }

    submitAndCheckNacks(looper, steward, op,
                        identifier=stewardSigner.verstr)


@pytest.mark.skipif(True, reason="Attribute encryption is done in client")
def testSponsorAddedAttributeIsEncrypted(addedEncryptedAttribute):
    pass


@pytest.mark.skipif(True, reason="Attribute Disclosure is not done for now")
def testSponsorDisclosesEncryptedAttribute(addedEncryptedAttribute, symEncData,
                                           looper, userSignerA, sponsorSigner,
                                           sponsor):
    box = libnacl.public.Box(sponsorSigner.naclSigner.keyraw,
                             userSignerA.naclSigner.verraw)

    data = json.dumps({SKEY: symEncData.secretKey,
                       TXN_ID: addedEncryptedAttribute[TXN_ID]})
    nonce, boxedMsg = box.encrypt(data.encode(), pack_nonce=False)

    op = {
        TARGET_NYM: userSignerA.verstr,
        TXN_TYPE: ATTRIB,
        NONCE: base58.b58encode(nonce),
        ENC: base58.b58encode(boxedMsg)
    }
    submitAndCheck(looper, sponsor, op,
                   identifier=sponsorSigner.verstr)


@pytest.mark.skipif(True, reason="Pending implementation")
def testSponsorAddedAttributeCanBeChanged(addedRawAttribute):
    # TODO but only by user(if user has taken control of his identity) and
    # sponsor
    raise NotImplementedError


def testGetAttribute(genned, addedSponsor, sponsorSigner,
                     sponsor, userSignerA, addedRawAttribute):
    assert sponsor.getAllAttributesForNym(userSignerA.verstr) == \
           [{'name': 'Mario'}]


def testLatestAttrIsReceived(genned, addedSponsor, sponsorSigner, looper,
                             sponsor, userSignerA):

    attr1 = {'name': 'Mario'}
    op = {
        TARGET_NYM: userSignerA.verstr,
        TXN_TYPE: ATTRIB,
        RAW: json.dumps(attr1)
    }
    submitAndCheck(looper, sponsor, op, identifier=sponsorSigner.verstr)
    assert sponsor.getAllAttributesForNym(userSignerA.verstr)[0] == attr1

    attr2 = {'name': 'Luigi'}
    op[RAW] = json.dumps(attr2)

    submitAndCheck(looper, sponsor, op, identifier=sponsorSigner.verstr)
    allAttributesForNym = sponsor.getAllAttributesForNym(userSignerA.verstr)
    assert allAttributesForNym[0] == attr2


@pytest.mark.skipif(True, reason="Test not implemented")
def testGetTxnsNoSeqNo():
    """
    Test GET_TXNS from client and do not provide any seqNo to fetch from
    """
    pass


def testGetTxnsSeqNo(genned, addedSponsor, tdir, sponsorSigner, looper):
    """
    Test GET_TXNS from client and provide seqNo to fetch from
    """
    sponsor = genTestClient(genned, signer=sponsorSigner, tmpdir=tdir)
    looper.add(sponsor)
    looper.run(sponsor.ensureConnectedToNodes())

    def chk():
        assert sponsor.spylog.count(sponsor.requestPendingTxns.__name__) > 0

    looper.run(eventually(chk, retryWait=1, timeout=3))
