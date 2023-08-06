import traceback

import pytest

import plenum
from plenum.common.raet import initLocalKeep
from plenum.test.eventually import eventually
from sovrin.client.wallet.link_invitation import LinkInvitation

plenum.common.util.loggingConfigured = False

from plenum.common.looper import Looper
from plenum.test.cli.helper import newKeyPair, checkAllNodesStarted, \
    checkCmdValid
from plenum.test.cli.conftest import nodeNames

from sovrin.common.util import getConfig
from sovrin.test.cli.helper import newCLI, ensureNodesCreated


config = getConfig()


@pytest.yield_fixture(scope="module")
def looper():
    with Looper(debug=False) as l:
        yield l


# TODO: Probably need to remove
@pytest.fixture("module")
def nodesCli(looper, tdir, nodeNames):
    cli = newCLI(looper, tdir)
    cli.enterCmd("new node all")
    checkAllNodesStarted(cli, *nodeNames)
    return cli


@pytest.fixture("module")
def cli(looper, tdir):
    return newCLI(looper, tdir)


@pytest.fixture(scope="module")
def stewardCreated(cli, createAllNodes, stewardSigner):
    steward = cli.newClient(clientName="steward", signer=stewardSigner)
    for node in cli.nodes.values():
        node.whitelistClient(steward.name)
    cli.looper.run(steward.ensureConnectedToNodes())
    return steward


@pytest.fixture(scope="module")
def newKeyPairCreated(cli):
    return newKeyPair(cli)


@pytest.fixture(scope="module")
def CliBuilder(tdir, tdirWithPoolTxns, tdirWithDomainTxns, tconf):
    def _(subdir, looper=None):
        def new():
            return newCLI(looper,
                          tdir,
                          subDirectory=subdir,
                          conf=tconf,
                          poolDir=tdirWithPoolTxns,
                          domainDir=tdirWithDomainTxns)
        if looper:
            yield new()
        else:
            with Looper(debug=False) as looper:
                yield new()
    return _


def getLinkInvitation(name, cli) -> LinkInvitation:
    existingLinkInvites = cli.activeWallet.getMatchingLinkInvitations(name)
    li = existingLinkInvites[0]
    return li


@pytest.fixture(scope="module")
def aliceMap():
    return {'keyring-name': 'Alice',
            }

@pytest.fixture(scope="module")
def faberMap():
    return {'inviter': 'Faber College',
            'invite': "sample/faber-invitation.sovrin",
            'invite-not-exists': "sample/faber-invitation.sovrin.not.exists",
            'inviter-not-exists': "non-existing-inviter",
            "target": "3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378KH4=",
            "nonce": "b1134a647eb818069c089e7694f63e6d",
            "endpoint": "0.0.0.0:1212",
            "claims" : "Transcript"
            }


@pytest.fixture(scope="module")
def loadInviteOut():
    return ["1 link invitation found for {inviter}.",
            "Creating Link for {inviter}.",
            "Generating Identifier and Signing key.",
            "Usage",
            'accept invitation "{inviter}"',
            'show link "{inviter}"']


@pytest.fixture(scope="module")
def fileNotExists():
    return ["Given file does not exist"]


@pytest.fixture(scope="module")
def connectedToTest():
    return ["Connected to test"]


@pytest.fixture(scope="module")
def canNotSyncMsg():
    return ["Cannot sync because not connected"]


@pytest.fixture(scope="module")
def syncWhenNotConnected(canNotSyncMsg, connectUsage):
    return canNotSyncMsg + connectUsage


@pytest.fixture(scope="module")
def canNotAcceptMsg():
    return ["Cannot accept because not connected"]


@pytest.fixture(scope="module")
def acceptWhenNotConnected(canNotAcceptMsg, connectUsage):
    return canNotAcceptMsg + connectUsage


@pytest.fixture(scope="module")
def acceptUnSyncedWhenConnected(commonAcceptInvitationMsgs):
    return commonAcceptInvitationMsgs + \
            ["Link {inviter} synced",
             "Starting communication with {inviter}"]


@pytest.fixture(scope="module")
def commonAcceptInvitationMsgs():
    return ["Invitation not yet verified",
            "Link not yet synchronized. Attempting to sync...",
            ]


@pytest.fixture(scope="module")
def acceptUnSyncedWhenNotConnected(commonAcceptInvitationMsgs,
                                       canNotSyncMsg, connectUsage):
    return commonAcceptInvitationMsgs + \
            ["Invitation acceptance aborted."] + \
            canNotSyncMsg + connectUsage


@pytest.fixture(scope="module")
def connectUsage():
    return ["Usage:",
            "  connect (live|test)"]


@pytest.fixture(scope="module")
def notConnectedStatus(connectUsage):
    return ['Not connected to any environment. Please connect first.'] +\
            connectUsage


@pytest.fixture(scope="module")
def newKeyringOut():
    return ["New keyring {keyring-name} created",
            'Active keyring set to "{keyring-name}"'
            ]


@pytest.fixture(scope="module")
def linkAlreadyExists():
    return ["Link already exists"]


@pytest.fixture(scope="module")
def linkNotExists():
    return ["No matching link invitation(s) found in current keyring"]


@pytest.fixture(scope="module")
def faberInviteLoaded(aliceCLI, be, do, faberMap, loadInviteOut):
    be(aliceCLI)
    do("load {invite}", expect=loadInviteOut, mapper=faberMap)


@pytest.fixture(scope="module")
def acmeMap():
    return {'inviter': 'Acme Corp',
            'invite': "sample/acme-job-application.sovrin",
            "target": "YSTHvR/sxdu41ig9mcqMq/DI5USQMVU4kpa6anJhot4=",
            "nonce": "57fbf9dc8c8e6acde33de98c6d747b28c",
            "claim-requests" : "Job Application"
            }


@pytest.fixture(scope="module")
def acmeInviteLoaded(aliceCLI, be, do, acmeMap, loadInviteOut):
    be(aliceCLI)
    do("load {invite}", expect=loadInviteOut, mapper=acmeMap)


@pytest.fixture(scope="module")
def attrAddedOut():
    return ["Attribute added for nym {target}"]


@pytest.fixture(scope="module")
def nymAddedOut():
    return ["Nym {target} added"]


@pytest.fixture(scope="module")
def unSyncedEndpointOut():
    return ["Target endpoint: <unknown, waiting for sync>"]


@pytest.fixture(scope="module")
def showLinkOutWithoutEndpoint(showLinkOut, unSyncedEndpointOut):
    return showLinkOut + unSyncedEndpointOut


@pytest.fixture(scope="module")
def endpointReceived():
    return ["Endpoint received:"]


@pytest.fixture(scope="module")
def endpointNotAvailable():
    return ["Endpoint not available"]



@pytest.fixture(scope="module")
def syncLinkOutEndsWith():
    return ["Link {inviter} synced"]


@pytest.fixture(scope="module")
def syncLinkOutStartsWith():
    return ["Synchronizing..."]


@pytest.fixture(scope="module")
def syncLinkOutWithEndpoint(syncLinkOutStartsWith, endpointReceived,
                            syncLinkOutEndsWith):
    return syncLinkOutStartsWith + endpointReceived + syncLinkOutEndsWith


@pytest.fixture(scope="module")
def syncLinkOutWithoutEndpoint(syncLinkOutStartsWith, endpointNotAvailable,
                               syncLinkOutEndsWith):
    return syncLinkOutStartsWith + endpointNotAvailable + syncLinkOutEndsWith


@pytest.fixture(scope="module")
def showSyncedLinkWithEndpointOut(showLinkOut):
    return showLinkOut + \
        ["Last synced: "] + \
        ["Target endpoint: {endpoint}"]


@pytest.fixture(scope="module")
def showSyncedLinkWithoutEndpointOut(showLinkOut):
    return showLinkOut + \
        ["Last synced: "] + \
        ["Target endpoint: Not Available"]


@pytest.fixture(scope="module")
def linkNotYetSynced():
    return ["Last synced: <this link has not yet been synchronized>"]


@pytest.fixture(scope="module")
def showUnSyncedLinkOut(showLinkOut, linkNotYetSynced):
    return showLinkOut + linkNotYetSynced


@pytest.fixture(scope="module")
def showAcceptedLinkOut():
    return [
            "Link",
            "Name: {inviter}",
            "Target: {target}",
            "Target Verification key: <same as target>",
            "Trust anchor: {inviter} (confirmed)",
            "Invitation nonce: {nonce}",
            "Invitation status: Accepted",
            "Available claims: {claims}",
            "Usage",
            'show claim {claims}',
            'request claim {claims}'
    ]


@pytest.fixture(scope="module")
def showLinkOut():
    return [
            "Link (not yet accepted)",
            "Name: {inviter}",
            "Target: {target}",
            "Target Verification key: <unknown, waiting for sync>",
            "Trust anchor: {inviter} (not yet written to Sovrin)",
            "Invitation nonce: {nonce}",
            "Invitation status: not verified, target verkey unknown",
            "Usage",
            'accept invitation "{inviter}"',
            'sync "{inviter}"']


@pytest.yield_fixture(scope="module")
def poolCLI_baby(CliBuilder):
    yield from CliBuilder("pool")


@pytest.yield_fixture(scope="module")
def aliceCLI(CliBuilder):
    yield from CliBuilder("alice")


@pytest.yield_fixture(scope="module")
def philCLI(CliBuilder):
    yield from CliBuilder("phil")


@pytest.fixture(scope="module")
def poolCLI(poolCLI_baby, poolTxnData, poolTxnNodeNames):
    seeds = poolTxnData["seeds"]
    for nName in poolTxnNodeNames:
        initLocalKeep(nName,
                      poolCLI_baby.basedirpath,
                      seeds[nName],
                      override=True)
    return poolCLI_baby


@pytest.fixture(scope="module")
def poolNodesCreated(poolCLI, poolTxnNodeNames):
    ensureNodesCreated(poolCLI, poolTxnNodeNames)
    return poolCLI


@pytest.fixture("module")
def ctx():
    """
    Provides a simple container for test context. Assists with 'be' and 'do'.
    """
    return {}


@pytest.fixture("module")
def be(ctx):
    """
    Fixture that is a 'be' function that closes over the test context.
    'be' allows to change the current cli in the context.
    """
    def _(cli):
        ctx['current_cli'] = cli
    return _


@pytest.fixture("module")
def do(ctx):
    """
    Fixture that is a 'do' function that closes over the test context
    'do' allows to call the do method of the current cli from the context.
    """
    def _(attempt, expect=None, within=None, mapper=None, not_expect=None):
        cli = ctx['current_cli']
        attempt = attempt.format(**mapper) if mapper else attempt
        checkCmdValid(cli, attempt)

        def check():
            nonlocal expect
            nonlocal not_expect

            def chk(obj, parity=True):
                if not obj:
                    return
                if isinstance(obj, str) or callable(obj):
                    obj = [obj]
                for e in obj:
                    if isinstance(e, str):
                        e = e.format(**mapper) if mapper else e
                        if parity:
                            assert e in cli.lastCmdOutput
                        else:
                            assert e not in cli.lastCmdOutput
                    elif callable(e):
                        # callables should raise exceptions to signal an error
                        if parity:
                            e(cli)
                        else:
                            try:
                                e(cli)
                            except:
                                # Since its a test so not using logger is not
                                # a big deal
                                traceback.print_exc()
                                continue
                            raise RuntimeError("did not expect success")
                    else:
                        raise AttributeError("only str, callable, or "
                                             "collections of str and callable "
                                             "are allowed")
            chk(expect)
            chk(not_expect, False)
        if within:
            cli.looper.run(eventually(check, timeout=within))
        else:
            check()
    return _


