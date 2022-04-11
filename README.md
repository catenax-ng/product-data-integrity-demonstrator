
# Introduction

This demonstrator showcases the need for a data integrity layer as a lower layer protocol which will be required in a cross-organization data eco system.


![KIKW Pyramid](https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/DIKW_Pyramid.svg/308px-DIKW_Pyramid.svg.png)

*Longlivetheux, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons*

The pyramid show how to gain information from data, knowledge from information and wisdom from knowledge.

Only pre-condidition: Hope that your input data is NOT "fake" data!

In the very very bad situation when your input data is "fake" data, you end up with something compared to "fake news"! And all efforts you build on top of it is worthless! You end up making business decisions on wrong or "fake data" (on purpose wrong or by accident wrong) and consequently you will end up with "fake information", "fake knowledge" and "fake wisdom"! So far so BAD, now you use all of this as input for business decisions?

In a cross-organization environment (data eco system) this is more important than ever before! In internal systems you have the control and "trust" in internal and internal central systems. In a cross-organization environment, additional measures need to be taken to increase the level of trust in the data exchanged!



Such an additional measure / effort is demonstrated in the following sections. It consists of 2 major building blocks:

- a hashed chain of data: This fits best to the picture that we follow in CX with building data "chains" along the supply chain. It helps to detect data changes (on purpose or by accident)

- 3rd party attestations (in the form of Verifiable Credentials): Nothing is worth more than an independent trusted 3rd party attestation on a "claim" someone makes (someone that you might not even know  - and definitely not trust - in such a data eco system). This is necessary to trust the data you receive. Technically, the very same thing that powers "Gaia X Labels" and "Self-Descriptions".

# Disclaimer
> The purpose of this repository is to showcase or demonstrate what data integrity is about. It is NOT meant to be used in any production like environment! We strongly recommend NOT to run this in a public network without additional security measures!

# Build instructions
```
DOCKER_BUILDKIT=0 docker-compose build
```
For the `acapy` service we need subdir-support (for the meantime while we are using a custom build of acapy) which is not yet possible in docker buildkit (or better: depends on your docker version or more precise, your buildkit version). Therefore we need to disable to get the fallback "old" build command.

The following error is an indication that you should disable buildkit:
```
failed to solve: rpc error: code = Unknown desc = failed to solve with frontend dockerfile.v0: failed to read dockerfile: failed to load cache key: subdir not supported yet
```

After a successful build:
```
docker-compose up
```

## Network considerations
If running locally with non-public hostnames, e.g. localhost, please use the same PORT for the backend inside and outside the container.
Also add a mapping to `/etc/hosts`
```
127.0.0.1       typetree-backend
```


# SupplyTree
This project implements the SupplyTree tamper evidence protocol described in detail here:
https://assets.bosch.com/media/global/research/eot/bosch-eot-paper-supplytree.pdf

A simple node structure looks like this
```
{
    "data": [
        {
            "url": "http://localhost:8000/data/d2d15e901e1142e277d3a70b4be6bdba95f30bd5495597127a261a65fe206cb1",
            "type": "http://supplytree.org/ns/ItemType"
        }
    ],
    "nodes": [],
    "previous": "http://localhost:8000/node/ed0ab2c7dab7b712526b60f8b2b7a3a2204192ac24d3a21aa6821574ef8189ec"
}
```
`data.type` can be used to decide whether it's worth to fetch the data or not from the given `data.url`.
Content behind `data.url` can be anything, but ideally, it is a standardized format (json / json-ld) that can be referred to in the `data.type` field.

`nodes` are references to supplier Tier-X data structures.

(Since this is the first implementation of the protocol, we decided to change the attribute name `references` -> `nodes` because we think the term better fits what it is)

`previous` is a reference to a historical previous version of the same thing, meaning at the same Tier-X level.
It does not refer to other organizations' data strctures. That's what `nodes` is for.

(`previous` is not described in the paper above.)

# TypeTree
TypeTree is a second layer on top of the very generic SupplyTree concept.

TypeTree builds a tamper-evidence Tree (or Graph) along the supply chain that holds basic information about (Part- / Material-) Types. Also known as PartNumber or in German: "Sachnummer".

Updates on those Types needs to be propagated downstream (forward...) in the the supply chain because eventually the information for customers (multiple levels downstream) has changed.

## CO2
The TypeTree alone often doesn't show any additional value to the user. Only connected with, e.g. CO2 equivalents, the TypeTree updates / versions might be of additional value.

This projects aims to showcase exactyly this.

# API
When the system is started, you can find the openapi endpoint at `/docs`

# Contributing
[CONTRIBUTING](./CONTRIBUTING.md)
