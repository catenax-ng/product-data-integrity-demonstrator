# most of those, taken from Swagger examples

CREATE_INVITATION_RESPONSE = """
{
  "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "invitation": {
    "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "@type": "https://didcomm.org/my-family/1.0/my-message-type",
    "did": "WgWxqztrNooG92RXvxSTWv",
    "imageUrl": "http://192.168.56.101/img/logo.jpg",
    "label": "Bob",
    "recipientKeys": [
      "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
    ],
    "routingKeys": [
      "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
    ],
    "serviceEndpoint": "http://192.168.56.101:8020"
  },
  "invitation_url": "http://192.168.56.101:8020/invite?c_i=eyJAdHlwZSI6Li4ufQ=="
}
"""

RECEIVE_INVITATION_RESPONSE = """
{
  "accept": "auto",
  "alias": "Bob, providing quotes",
  "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "connection_protocol": "connections/1.0",
  "created_at": "2021-12-31T23:59:59Z",
  "error_msg": "No DIDDoc provided; cannot connect to public DID",
  "inbound_connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "invitation_key": "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV",
  "invitation_mode": "once",
  "invitation_msg_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "my_did": "WgWxqztrNooG92RXvxSTWv",
  "request_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "rfc23_state": "invitation-sent",
  "routing_state": "active",
  "state": "active",
  "their_did": "WgWxqztrNooG92RXvxSTWv",
  "their_label": "Bob",
  "their_public_did": "2cpBmR3FqGKWi5EyUbpRY8",
  "their_role": "requester",
  "updated_at": "2021-12-31T23:59:59Z"
}
"""
CONNECTION_DETAILS_RESPONSE = """
{
  "accept": "auto",
  "alias": "Bob, providing quotes",
  "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "connection_protocol": "connections/1.0",
  "created_at": "2021-12-31T23:59:59Z",
  "error_msg": "No DIDDoc provided; cannot connect to public DID",
  "inbound_connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "invitation_key": "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV",
  "invitation_mode": "once",
  "invitation_msg_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "my_did": "WgWxqztrNooG92RXvxSTWv",
  "request_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "rfc23_state": "invitation-sent",
  "routing_state": "active",
  "state": "active",
  "their_did": "WgWxqztrNooG92RXvxSTWv",
  "their_label": "Bob",
  "their_public_did": "2cpBmR3FqGKWi5EyUbpRY8",
  "their_role": "requester",
  "updated_at": "2021-12-31T23:59:59Z"
}
"""
ISSUE_CREDENTIAL_2_SEND_RESPONSE = """
{
    "auto_issue": false,
    "auto_offer": false,
    "auto_remove": false,
    "by_format": {
      "cred_issue": {},
      "cred_offer": {},
      "cred_proposal": {},
      "cred_request": {}
    },
    "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2021-12-31T23:59:59Z",
    "cred_ex_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "cred_issue": {
      "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "@type": "https://didcomm.org/my-family/1.0/my-message-type",
      "comment": "string",
      "credentials~attach": [
        {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "byte_count": 1234,
          "data": {
            "base64": "ey4uLn0=",
            "json": {"sample": "content"},
            "jws": {
              "header": {
                "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
              },
              "protected": "ey4uLn0",
              "signature": "ey4uLn0",
              "signatures": [
                {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0"
                }
              ]
            },
            "links": [
              "https://link.to/data"
            ],
            "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
          },
          "description": "view from doorway, facing east, with lights off",
          "filename": "IMG1092348.png",
          "lastmod_time": "2021-12-31T23:59:59Z",
          "mime-type": "image/png"
        }
      ],
      "formats": [
        {
          "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "format": "aries/ld-proof-vc-detail@v1.0"
        }
      ],
      "replacement_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    },
    "cred_offer": {
      "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "@type": "https://didcomm.org/my-family/1.0/my-message-type",
      "comment": "string",
      "credential_preview": {
        "@type": "issue-credential/2.0/credential-preview",
        "attributes": [
          {
            "mime-type": "image/jpeg",
            "name": "favourite_drink",
            "value": "martini"
          }
        ]
      },
      "formats": [
        {
          "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "format": "aries/ld-proof-vc-detail@v1.0"
        }
      ],
      "offers~attach": [
        {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "byte_count": 1234,
          "data": {
            "base64": "ey4uLn0=",
            "json": {"sample": "content"},
            "jws": {
              "header": {
                "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
              },
              "protected": "ey4uLn0",
              "signature": "ey4uLn0",
              "signatures": [
                {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0"
                }
              ]
            },
            "links": [
              "https://link.to/data"
            ],
            "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
          },
          "description": "view from doorway, facing east, with lights off",
          "filename": "IMG1092348.png",
          "lastmod_time": "2021-12-31T23:59:59Z",
          "mime-type": "image/png"
        }
      ],
      "replacement_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    },
    "cred_preview": {
      "@type": "issue-credential/2.0/credential-preview",
      "attributes": [
        {
          "mime-type": "image/jpeg",
          "name": "favourite_drink",
          "value": "martini"
        }
      ]
    },
    "cred_proposal": {
      "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "@type": "https://didcomm.org/my-family/1.0/my-message-type",
      "comment": "string",
      "credential_preview": {
        "@type": "issue-credential/2.0/credential-preview",
        "attributes": [
          {
            "mime-type": "image/jpeg",
            "name": "favourite_drink",
            "value": "martini"
          }
        ]
      },
      "filters~attach": [
        {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "byte_count": 1234,
          "data": {
            "base64": "ey4uLn0=",
            "json": {"sample": "content"},
            "jws": {
              "header": {
                "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
              },
              "protected": "ey4uLn0",
              "signature": "ey4uLn0",
              "signatures": [
                {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0"
                }
              ]
            },
            "links": [
              "https://link.to/data"
            ],
            "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
          },
          "description": "view from doorway, facing east, with lights off",
          "filename": "IMG1092348.png",
          "lastmod_time": "2021-12-31T23:59:59Z",
          "mime-type": "image/png"
        }
      ],
      "formats": [
        {
          "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "format": "aries/ld-proof-vc-detail@v1.0"
        }
      ]
    },
    "cred_request": {
      "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "@type": "https://didcomm.org/my-family/1.0/my-message-type",
      "comment": "string",
      "formats": [
        {
          "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "format": "aries/ld-proof-vc-detail@v1.0"
        }
      ],
      "requests~attach": [
        {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "byte_count": 1234,
          "data": {
            "base64": "ey4uLn0=",
            "json": {"sample": "content"},
            "jws": {
              "header": {
                "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
              },
              "protected": "ey4uLn0",
              "signature": "ey4uLn0",
              "signatures": [
                {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0"
                }
              ]
            },
            "links": [
              "https://link.to/data"
            ],
            "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
          },
          "description": "view from doorway, facing east, with lights off",
          "filename": "IMG1092348.png",
          "lastmod_time": "2021-12-31T23:59:59Z",
          "mime-type": "image/png"
        }
      ]
    },
    "error_msg": "The front fell off",
    "initiator": "self",
    "parent_thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "role": "issuer",
    "state": "done",
    "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "trace": true,
    "updated_at": "2021-12-31T23:59:59Z"
  }
"""
PRESENT_PROOF_2_SEND_REQUEST_RESPONSE = """
{
    "auto_present": false,
    "by_format": {
      "pres": {},
      "pres_proposal": {},
      "pres_request": {}
    },
    "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2021-12-31T23:59:59Z",
    "error_msg": "Invalid structure",
    "initiator": "self",
    "pres": {
      "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "@type": "https://didcomm.org/my-family/1.0/my-message-type",
      "comment": "string",
      "formats": [
        {
          "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "format": "dif/presentation-exchange/submission@v1.0"
        }
      ],
      "presentations~attach": [
        {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "byte_count": 1234,
          "data": {
            "base64": "ey4uLn0=",
            "json": {"sample": "content"},
            "jws": {
              "header": {
                "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
              },
              "protected": "ey4uLn0",
              "signature": "ey4uLn0",
              "signatures": [
                {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0"
                }
              ]
            },
            "links": [
              "https://link.to/data"
            ],
            "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
          },
          "description": "view from doorway, facing east, with lights off",
          "filename": "IMG1092348.png",
          "lastmod_time": "2021-12-31T23:59:59Z",
          "mime-type": "image/png"
        }
      ]
    },
    "pres_ex_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "pres_proposal": {
      "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "@type": "https://didcomm.org/my-family/1.0/my-message-type",
      "comment": "string",
      "formats": [
        {
          "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "format": "dif/presentation-exchange/submission@v1.0"
        }
      ],
      "proposals~attach": [
        {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "byte_count": 1234,
          "data": {
            "base64": "ey4uLn0=",
            "json": {"sample": "content"},
            "jws": {
              "header": {
                "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
              },
              "protected": "ey4uLn0",
              "signature": "ey4uLn0",
              "signatures": [
                {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0"
                }
              ]
            },
            "links": [
              "https://link.to/data"
            ],
            "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
          },
          "description": "view from doorway, facing east, with lights off",
          "filename": "IMG1092348.png",
          "lastmod_time": "2021-12-31T23:59:59Z",
          "mime-type": "image/png"
        }
      ]
    },
    "pres_request": {
      "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "@type": "https://didcomm.org/my-family/1.0/my-message-type",
      "comment": "string",
      "formats": [
        {
          "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "format": "dif/presentation-exchange/submission@v1.0"
        }
      ],
      "request_presentations~attach": [
        {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "byte_count": 1234,
          "data": {
            "base64": "ey4uLn0=",
            "json": {"sample": "content"},
            "jws": {
              "header": {
                "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
              },
              "protected": "ey4uLn0",
              "signature": "ey4uLn0",
              "signatures": [
                {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0"
                }
              ]
            },
            "links": [
              "https://link.to/data"
            ],
            "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
          },
          "description": "view from doorway, facing east, with lights off",
          "filename": "IMG1092348.png",
          "lastmod_time": "2021-12-31T23:59:59Z",
          "mime-type": "image/png"
        }
      ],
      "will_confirm": true
    },
    "role": "prover",
    "state": "proposal-sent",
    "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "trace": true,
    "updated_at": "2021-12-31T23:59:59Z",
    "verified": "true"
  }
"""
PRESENT_PROOF_2_RECORDS_RESPONSE = """
{
    "results": [
      {
        "auto_present": false,
        "by_format": {
          "pres": {},
          "pres_proposal": {},
          "pres_request": {}
        },
        "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-12-31T23:59:59Z",
        "error_msg": "Invalid structure",
        "initiator": "self",
        "pres": {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "@type": "https://didcomm.org/my-family/1.0/my-message-type",
          "comment": "string",
          "formats": [
            {
              "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "format": "dif/presentation-exchange/submission@v1.0"
            }
          ],
          "presentations~attach": [
            {
              "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "byte_count": 1234,
              "data": {
                "base64": "ey4uLn0=",
                "json": {"sample": "content"},
                "jws": {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0",
                  "signatures": [
                    {
                      "header": {
                        "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                      },
                      "protected": "ey4uLn0",
                      "signature": "ey4uLn0"
                    }
                  ]
                },
                "links": [
                  "https://link.to/data"
                ],
                "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
              },
              "description": "view from doorway, facing east, with lights off",
              "filename": "IMG1092348.png",
              "lastmod_time": "2021-12-31T23:59:59Z",
              "mime-type": "image/png"
            }
          ]
        },
        "pres_ex_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "pres_proposal": {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "@type": "https://didcomm.org/my-family/1.0/my-message-type",
          "comment": "string",
          "formats": [
            {
              "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "format": "dif/presentation-exchange/submission@v1.0"
            }
          ],
          "proposals~attach": [
            {
              "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "byte_count": 1234,
              "data": {
                "base64": "ey4uLn0=",
                "json": {"sample": "content"},
                "jws": {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0",
                  "signatures": [
                    {
                      "header": {
                        "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                      },
                      "protected": "ey4uLn0",
                      "signature": "ey4uLn0"
                    }
                  ]
                },
                "links": [
                  "https://link.to/data"
                ],
                "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
              },
              "description": "view from doorway, facing east, with lights off",
              "filename": "IMG1092348.png",
              "lastmod_time": "2021-12-31T23:59:59Z",
              "mime-type": "image/png"
            }
          ]
        },
        "pres_request": {
          "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "@type": "https://didcomm.org/my-family/1.0/my-message-type",
          "comment": "string",
          "formats": [
            {
              "attach_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "format": "dif/presentation-exchange/submission@v1.0"
            }
          ],
          "request_presentations~attach": [
            {
              "@id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "byte_count": 1234,
              "data": {
                "base64": "ey4uLn0=",
                "json": {"sample": "content"},
                "jws": {
                  "header": {
                    "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                  },
                  "protected": "ey4uLn0",
                  "signature": "ey4uLn0",
                  "signatures": [
                    {
                      "header": {
                        "kid": "did:sov:LjgpST2rjsoxYegQDRm7EL#keys-4"
                      },
                      "protected": "ey4uLn0",
                      "signature": "ey4uLn0"
                    }
                  ]
                },
                "links": [
                  "https://link.to/data"
                ],
                "sha256": "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"
              },
              "description": "view from doorway, facing east, with lights off",
              "filename": "IMG1092348.png",
              "lastmod_time": "2021-12-31T23:59:59Z",
              "mime-type": "image/png"
            }
          ],
          "will_confirm": true
        },
        "role": "prover",
        "state": "proposal-sent",
        "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "trace": true,
        "updated_at": "2021-12-31T23:59:59Z",
        "verified": "true"
      }
    ]
  }
"""
CONNECTIONS_RESPONSE = """
{
  "results": [
    {
      "accept": "auto",
      "alias": "Bob, providing quotes",
      "connection_id": "conn1",
      "connection_protocol": "connections/1.0",
      "created_at": "2021-12-31T23:59:59Z",
      "error_msg": "No DIDDoc provided; cannot connect to public DID",
      "inbound_connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "invitation_key": "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV",
      "invitation_mode": "once",
      "invitation_msg_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "my_did": "WgWxqztrNooG92RXvxSTWv",
      "request_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "rfc23_state": "invitation-sent",
      "routing_state": "active",
      "state": "active",
      "their_did": "WgWxqztrNooG92RXvxSTWv",
      "their_label": "Bob",
      "their_public_did": "2cpBmR3FqGKWi5EyUbpRY8",
      "their_role": "requester",
      "updated_at": "2021-12-31T23:59:59Z"
    }
  ]
}
"""