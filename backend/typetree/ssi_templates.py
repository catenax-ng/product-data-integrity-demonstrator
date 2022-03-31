# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

NONCE_PRESENTATION_REQUEST = """
{
    "comment": "Please reply with your NONCE VC",
    "connection_id": "",
    "presentation_request": {
        "dif": {
            "options": {
                "challenge": "1ec8dfcb-a51e-48fb-aa21-6bbccf44ce64",
                "domain": ""
            },
            "presentation_definition": {
                "id": "32f54163-7166-48f1-93d8-ff217bdb0654",
                "format": {
                    "ldp_vp": {
                        "proof_type": [
                            "Ed25519Signature2018"
                        ]
                    }
                },
                "input_descriptors": [
                    {
                        "id": "nonce_reply",
                        "name": "Nonce Reply Message",
                        "schema": [
                            {
                                "uri": "https://www.w3.org/2018/credentials#VerifiableCredential"
                            }
                        ],
                        "constraints": {
                            "is_holder": [
                                {
                                    "directive": "required",
                                    "field_id": [
                                        "f1d059bd-09a5-4097-ade9-947126d72d81"
                                    ]
                                }
                            ],
                            "fields": [
                                {
                                    "id": "f1d059bd-09a5-4097-ade9-947126d72d81",
                                    "path": [
                                        "$.nonce"
                                    ],
                                    "purpose": "See whether this is an answer to our question"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }
}
"""

ISSUE_SEND_REQUEST = """
{
    "auto_remove": true,
    "comment": "Please check data and issue VC for it",
    "connection_id": "",
    "filter": {
      "ld_proof": {
        "credential": {
          "@context": [
            "https://www.w3.org/2018/credentials/v1",
            {
                "st": "http://supplytree.org/ns#",
                "ContentConfirmationCredential": "st:ContentConfirmationCredential",
                "nodeId": "st:nodeId",
                "dataId": "st:dataId",
                "dataType": "st:dataType",
                "dataKey": "st:dataKey",
                "dataValue": "st:dataValue"
              }
    
          ],
          "credentialSubject": {
            "nodeId": "",
            "dataId": "",
            "dataKey": "",
            "dataValue": ""
          },
          "issuanceDate": "",
          "issuer": "",
          "type": [
            "VerifiableCredential",
            "ContentConfirmationCredential"
          ]
        },
        "options": {
          "proofType": "Ed25519Signature2018"
        }
      }
    },
    "holder_did": "",
    "trace": true
  }
"""

ISSUE_SEND_REQUEST_CO2 = """
{
    "auto_remove": true,
    "comment": "Please check CO2 along the chain and issue VC for it",
    "connection_id": "",
    "filter": {
      "ld_proof": {
        "credential": {
          "@context": [
            "https://www.w3.org/2018/credentials/v1",
            {
                "st": "http://supplytree.org/ns#",
                "Co2ConfirmationCredential": "st:Co2ConfirmationCredential",
                "nodeId": "st:nodeId",
                "co2Sum": "st:co2Sum"
              }
    
          ],
          "credentialSubject": {
            "nodeId": "",
            "co2Sum": ""
          },
          "issuanceDate": "",
          "issuer": "",
          "type": [
            "VerifiableCredential",
            "Co2ConfirmationCredential"
          ]
        },
        "options": {
          "proofType": "Ed25519Signature2018"
        }
      }
    },
    "holder_did": "",
    "trace": true
  }
"""

CO2_PRESENTATION_REQUEST = """
{
    "comment": "Please provide CO2 Sum for the entire value chain",
    "connection_id": "",
    "presentation_request": {
        "dif": {
            "options": {
                "challenge": "ec982e22-1689-48c6-be3a-bf93297b3425",
                "domain": ""
            },
            "presentation_definition": {
                "id": "f117e520-6850-41fe-b783-a83bba994b8a",
                "format": {
                    "ldp_vp": {
                        "proof_type": [
                            "Ed25519Signature2018"
                        ]
                    }
                },
                "input_descriptors": [
                    {
                        "id": "co2_sum",
                        "name": "CO2 Sum",
                        "schema": [
                            {
                                "uri": "https://www.w3.org/2018/credentials#VerifiableCredential"
                            }
                        ],
                        "constraints": {
                            "is_holder": [
                                {
                                    "directive": "required",
                                    "field_id": [
                                        "230ca2dc-52d8-469a-9daa-b825d3c0e70d",
                                        "3c4cc003-0c00-4df8-bd3a-2fc8e48c9af3"
                                    ]
                                }
                            ],
                            "fields": [
                                {
                                    "id": "230ca2dc-52d8-469a-9daa-b825d3c0e70d",
                                    "path": [
                                        "$.credentialSubject.nodeId"
                                    ],
                                    "purpose": "The unique entry point for the CO2 Sum",
                                    "filter": {
                                        "type": "string",
                                        "pattern": "<node_id_url>"
                                    }
                                },
                                {
                                    "id": "3c4cc003-0c00-4df8-bd3a-2fc8e48c9af3",
                                    "path": [
                                        "$.credentialSubject.co2Sum"
                                    ],
                                    "purpose": "The CO2 sum of the chain"
                                }

                            ]
                        }
                    }
                ]
            }
        }
    }
}
"""

CO2_PRESENTATION_REQUEST_SEND = """
{
  "dif": {
    "record_ids": {
      "co2_sum": [
          "<credential_id>"
      ]
    }
  },
  "trace": true
}
"""