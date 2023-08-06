ACCEPT_INVITE = 'ACCEPT_INVITE'
AVAIL_CLAIM_LIST = 'AVAIL_CLAIM_LIST'
REQUEST_CLAIMS = 'REQUEST_CLAIMS'
CLAIMS = 'CLAIMS'


"""
ACCEPT_INVITE
{
    "type": 'ACCEPT_INVITE',
    "identifier": <id>,
    "nonce": <nonce>,
    "signature" : <sig>
}


AVAIL_CLAIM_LIST
{
    'type': 'AVAIL_CLAIM_LIST',
    'claims_list': [
        "Name": "Transcript",
        "Version": "1.2",
        "Definition": {
            "Attributes": {
                "student_name": "string",
                "ssn": "int",
                "degree": "string",
                "year": "string",
                "status": "string"
            }
        }
    ],
    "signature" : <sig>
}

AVAIL_CLAIM_LIST
{
    'type': 'AVAIL_CLAIM_LIST',
    'claims_list': [
        "Name": "Transcript",
        "Version": "1.2",
        "Definition": {
            "Attributes": {
                "student_name": "string",
                "ssn": "int",
                "degree": "string",
                "year": "string",
                "status": "string"
            }
        }
    ],
    "signature" : <sig>
}

"""
