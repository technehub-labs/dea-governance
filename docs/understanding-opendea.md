# Understanding OpenDEA: A Plain-Language Guide

This guide explains what the OpenDEA catalogs contain, how the entity types connect, and why the system is structured the way it is — without requiring technical knowledge of schemas, gates, or CR processes.

---

## The big picture

OpenDEA is a set of ** interconnected catalogs** that describe how an enterprise works. Think of them as a very detailed, structured map of the organization. Each catalog holds one type of information — capabilities, processes, people, technology, money, information itself — and they all reference each other.

The system is built from **entity types** defined in a single **metamodel**. Every catalog instantiates one or more of these entity types. Currently, the org has **44 catalog repositories** covering **163 entity types** and **121 relationship types**, with **9,699 records** across the populated catalogs.

---

## The information family

Information in the enterprise is modeled through four connected entity types:

### Business Object
The **real-world thing the business cares about** — a Customer, an Order, an Invoice, a Network Asset. If you can point at it and say "the enterprise has one of those," it's a business object.

### Information Model
The **blueprint** that says what attributes a business object has, what rules constrain it, and how it connects to other objects. Think of it as the architect's drawing: it doesn't hold the data, it defines the *shape* of the data.

### Information Asset
The **consumable form** the information takes when someone uses it — a report, a dashboard, an invoice document, a data feed. If you can email it or display it on a screen, it's an information asset.

### Data Entity
The **physical structure** where the information is stored — a database table, a document store, a graph node. This is the IT-level implementation of the blueprint.

**How they connect:**
```
Business Object ("we have Customers")
    ↓ represented by
Information Model ("a Customer has: id, name, segments, status")
    ↓ structures
Data Entity ("the CRM database table stores Customers")
    ↓ contextualized into
Information Asset ("the Q3 customer review report")
```

### Information Class
Alongside this family, **Information Classes** are the **sensitivity and regulatory bands** that information falls into: public, internal, confidential, restricted; PII, PHI, PCI. Every piece of information can be *mapped to* a class, which determines how it must be handled.

---

## The commercial chain

Business objects sit on a **decomposition chain** that mirrors how an enterprise turns agreements into value:

| Stage | What it means | Example business objects |
|---|---|---|
| **Agreement** | Contracts and permissions that bind parties | Contract, License, Consent Record |
| **Offering** | What the enterprise offers to the market | Price List, Tariff Plan, Subscription |
| **Product** | Tangible or intangible things the enterprise sells | Product, SKU, Requirement |
| **Service** | Activities the enterprise performs | Service, Service Instance |
| **Resource** | Assets used to deliver | Network Asset, Machine, SIM Profile |
| **Entity** | The persistent records | Application, Configuration Item, Journal Entry |

Each **Information Model** records which stage its business object sits on. When you look at the model corpus, you can see the enterprise's information organized by this chain — from the contracts at the top to the operational records at the bottom.

---

## The other entity families

Beyond information, the org models:

- **Business Capabilities** — what the enterprise *can do* (40 canonical: Asset Management, Customer Management, Risk Management...)
- **Business Processes** — *how* it does it (3,722 records across the 7×7 ECF matrix)
- **Actors and Roles** — *who* does it (humans, teams, AI agents)
- **Controls and Regulations** — *what constrains it* (20 controls, 8 regulations)
- **Value Streams** — *how value flows* end-to-end (111 records)
- **Knowledge Assets** — the org's *accumulated know-how* (standards, method documents)

---

## How it's kept honest

Every record goes through an **evidence ladder**: it starts as a candidate, gets corroborated against a verifiable source, is reviewed, and only then becomes canonical. Gates in CI check that records are well-formed, relationships are valid, and the documentation matches the data. A weekly reconciler checks that the portfolio register matches GitHub reality.

The system is designed so that **absence is honest**: if a relationship hasn't been asserted yet (because the target catalog doesn't exist, or the evidence isn't available), the record says so explicitly rather than inventing a placeholder.

---

## Key numbers (2026-11-02)

| What | Count |
|---|---|
| Catalog repositories | 44 |
| Canonical records (org-wide) | 9,699 |
| Business capabilities | 40 |
| Business processes (L2) | 146 (146/146 IO-complete) |
| Information models | 74 (100% BO coverage) |
| Information assets | 25 |
| Controls | 20 |
| Business objects | 74 |
| Information classes | 8 |
| Regulations | 8 |
| Knowledge assets | 8 |
| Value streams | 111 |
