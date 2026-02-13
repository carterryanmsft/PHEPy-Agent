# IC/MCS Customer Lookup Guide

**Purpose**: Quick reference for customer identification and query optimization

**Source**: `IC and MCS 2.4.csv` (authoritative contact list)

---

## 🎯 Quick Lookup Table

| Customer | TenantId | TPID | Program | CLE | PHE |
|----------|----------|------|---------|-----|-----|
| **ADNOC** | 74892fe7-b6cb-43e7-912b-52194d3fd7c8 | 521755 | MCS | Prashant Shanbhag | Angelo Oliveira |
| **Amazon** | 5280104a-472d-4538-9ccf-1e1d0efe8b1b | 915327 | MCS | Cosmin Guliman | Kanika Kapoor |
| **Barclays Bank** | c4b62f1d-01e0-4107-a0cc-5ac886858b23 | 1835064 | MCS | Angelo Oliveira | Neill O'Keeffe |
| **EY** | 5b973f99-77df-4beb-b27d-aa0c70b8482c | 636852 | MCS | JJ Streicher-Bremer | Ramana Krishnamoorthy |
| **Morgan Stanley** | 03beb921-c16c-4a69-a0df-0c9b1fb22415 | 642489 | MCS | Serina Vartanian | Ron Mustard |
| **National Health Service** | 37c354b2-85b0-47f5-b222-07b48d774ee3 | 522086 | MCS | Pavel Garmashov | Karthik Muthiah R |
| **Palantir** | 76463010-5dd7-40c7-b509-7ce28ba39430 | 11926445 | MCS | Steven Andress | Hemanth Varyani |
| **Walmart** | 3cbcc3d3-094d-4006-9849-0d11d61f484d | 784852 | MCS | Steven Andress | Tim Griffin |
| **Ford** | c990bb7a-51f4-439b-bd36-9c07fb1041c0 | 639534 | IC | - | Ron Mustard |
| **Sainsbury's** | e11fd634-26b5-47f4-8b8c-908e466e9bdf | 7056084 | IC | - | Sonal Sagar |
| **Autodesk** | 67bff79e-7f91-4433-a8e5-c9252d2ddc1d | 625338 | IC | - | Tim Griffin |
| **Vodafone** | 68283f3b-8487-4c86-adb3-a5228f18b893 | 520413 | IC | - | Josef Ibarra |
| **State of WA** | 11d0e217-264e-400a-8ba0-57dcc127d72d | 641135 | IC | - | Kanika Kapoor |
| **BHP** | 4f6e1565-c2c7-43cb-8a4c-0981d022ce20 | 523272 | IC | - | Manaswi Upadhyaya K |
| **AGL Energy** | 123913b9-915d-4d67-aaf9-ce327e8fc59f | 1170498 | IC | - | Maathangi Kannan Vaidehi |
| **WSP** | 3d234255-e20f-4205-88a5-9658a402999b | 2831650 | IC | - | Amulya Eedara |
| **Huntington** | 157a26ef-912f-4244-abef-b45fc4bd77f9 | 645695 | IC | - | Hemanth Varyani |
| **Nestle** | 12a3af23-a769-4654-847f-958f3d479f4a | 604010 | IC | - | Josef Ibarra |
| **Santander** | 35595a02-4d6d-44ac-99e1-f9ab4cd872db | 1278397 | IC | - | Pavel Garmashov |
| **Zurich** | 95d1d810-50cf-4169-8565-6bfba279a0cd | 2656229 | IC | - | Pavel Garmashov |
| **Novartis** | f35a6974-607f-47d4-82d7-ff31d7dc53a5 | 1528952 | IC | - | Ramana Krishnamoorthy |
| **NAB** | 48d6943f-580e-40b1-a0e1-c07fa3707873 | 1104955 | IC | - | KAPIL Chopra |
| **MUFJ** | 3a498a73-f68c-4993-9940-40f5dc4b029b | 5025483 | IC | - | Salonie Vyas |

**Note**: 
- Some customers have multiple TenantIds (see full CSV for complete list)
- CLE column empty for IC customers (IC program doesn't use CLE role)
- **CLE** = Customer Lead Engineer
- **PHE** = Product Health Engineer

---

## 🔍 Customer Name Variations

**Common Aliases** (use TenantId instead of searching by name):

| Official Name | Common Variations | TenantId (Use This!) |
|---------------|-------------------|----------------------|
| Ford | Ford, FORD MOTOR COMPANY, Azureford, Ford Motor Co | c990bb7a-51f4-439b-bd36-9c07fb1041c0 |
| Amazon | Amazon, AMAZON.COM, AWS, Amazon Web Services | 5280104a-472d-4538-9ccf-1e1d0efe8b1b |
| Walmart | Walmart, WAL-MART, Wal-Mart Stores Inc | 3cbcc3d3-094d-4006-9849-0d11d61f484d |
| State of WA | State of Washington, WA State, Washington State | 11d0e217-264e-400a-8ba0-57dcc127d72d |
| National Health Service | NHS, NHS UK, National Health Service UK | 37c354b2-85b0-47f5-b222-07b48d774ee3 |
| Morgan Stanley | MS, Morgan Stanley & Co | 03beb921-c16c-4a69-a0df-0c9b1fb22415 |

**Rule**: Always query by `TenantId`, never by customer name variations!

---

## 📋 Lookup Process

### Step 1: Identify Customer
```
User asks: "How many cases does Ford have?"
               ↓
Parse: Customer = "Ford"
```

### Step 2: Read Contact File
```kusto
// Read: grounding_docs/contacts_access/IC and MCS 2.4.csv
// Find row where: TopParentName == "Ford"
```

### Step 3: Extract TenantId
```
TopParentName: Ford
TenantId: c990bb7a-51f4-439b-bd36-9c07fb1041c0
TPID: 639534
Program: IC
PHE: Ron Mustard
```

### Step 4: Use in Query
```kusto
GetSCIMIncidentV2
| where TenantId == "c990bb7a-51f4-439b-bd36-9c07fb1041c0"  // Ford
| where ServiceRequestState != "Closed"
...
```

---

## 🎯 Multi-Tenant Customers

**Customers with Multiple TenantIds**:

### Walmart (8 TenantIds):
```
3cbcc3d3-094d-4006-9849-0d11d61f484d
b3fddaa6-c66f-4dc6-acec-aee02fd27d25
af82106b-f60a-4242-8e57-216d39d26b7d
e96e5039-f1ad-4b4d-8d8f-d42084607ae2
4d75fb71-9099-4d4b-b774-7346d1eb2563
c8cc070e-dfed-45c9-bda5-29d00121acbb
2ce79a24-c41a-4e48-838b-c6eea361762e
f6f3eefa-6b96-4d00-8389-192378d54e1f
```

**Query Pattern**:
```kusto
| where TenantId in (
    "3cbcc3d3-094d-4006-9849-0d11d61f484d",
    "b3fddaa6-c66f-4dc6-acec-aee02fd27d25",
    // ... all 8 TenantIds
)
```

### State of WA (2 TenantIds):
```
11d0e217-264e-400a-8ba0-57dcc127d72d
9ef85bca-98dd-4e6e-b55c-f296e678e989
```

### Morgan Stanley (2 TenantIds):
```
03beb921-c16c-4a69-a0df-0c9b1fb22415
e29b8111-49f8-418d-ac2a-935335a52614
```

### MUFJ (2 TenantIds):
```
3a498a73-f68c-4993-9940-40f5dc4b029b
952d7d55-02c8-4421-ae6d-aa79da2f5152
```

---

## 🚫 Common Mistakes

### ❌ DON'T:
```kusto
// Bad: Searching by customer name (unreliable)
| where CustomerName == "Ford"
| where CustomerName contains "Ford Motor"
| where TopParentName == "Azureford"

// Bad: Hardcoded names (variations exist)
| where CustomerName in ("Ford", "FORD", "Ford Motor")
```

### ✅ DO:
```kusto
// Good: Use TenantId (canonical, unique, indexed)
| where TenantId == "c990bb7a-51f4-439b-bd36-9c07fb1041c0"

// Good: For multi-tenant customers
| where TenantId in (
    "3cbcc3d3-094d-4006-9849-0d11d61f484d",
    "b3fddaa6-c66f-4dc6-acec-aee02fd27d25"
)
```

---

## 📊 Program Breakdown

| Program | Customer Count | Description |
|---------|----------------|-------------|
| **MCS** (Microsoft Consulting Services) | 8 | Enterprise customers with dedicated CLE + PHE |
| **IC** (Intensive Care) | 15 | High-priority customers with dedicated PHE |

**Difference**:
- **MCS**: Both CLE and PHE assigned
- **IC**: PHE only, no CLE

---

## 🔗 Integration with Kusto

### Datatable Pattern (For Multi-Customer Queries):
```kusto
let ICMCSTenants = datatable(TopParentName:string, TenantId:string, PHE:string, Program:string)
[
    "Ford", "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "Ron Mustard", "IC",
    "Amazon", "5280104a-472d-4538-9ccf-1e1d0efe8b1b", "Kanika Kapoor", "MCS",
    "Walmart", "3cbcc3d3-094d-4006-9849-0d11d61f484d", "Tim Griffin", "MCS",
    // ... include all customers
];

GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| join kind=inner ICMCSTenants on TenantId
| summarize Cases = count() by TopParentName, PHE, Program
| order by Cases desc
```

---

## 📞 Contact Information

### When User Asks: "Who is the PHE for [Customer]?"

**Response Template**:
```
[Customer] Contact Information:
- Product Health Engineer (PHE): [Name]
- Customer Lead Engineer (CLE): [Name or "N/A - IC customer"]
- TPID: [ID]
- Program: [IC/MCS]
- TenantId: [UUID]
```

**Example**:
```
Amazon Contact Information:
- Product Health Engineer (PHE): Kanika Kapoor
- Customer Lead Engineer (CLE): Cosmin Guliman
- TPID: 915327
- Program: MCS
- TenantId: 5280104a-472d-4538-9ccf-1e1d0efe8b1b
```

---

## 🔄 Refresh Process

**Source File**: `grounding_docs/contacts_access/IC and MCS 2.4.csv`

**Update Frequency**: Monthly (or as notified)

**When Updated**:
1. Re-read CSV file
2. Update this lookup guide with new customers
3. Update Kusto datatable definitions in query files

---

**Last Updated**: February 4, 2026  
**Maintained By**: Contacts & Escalation Finder Sub-Agent  
**Source**: IC and MCS 2.4.csv (24 customers, 38 total tenants)
