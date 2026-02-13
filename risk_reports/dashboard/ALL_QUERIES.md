# All Dashboard Queries - Copy/Paste Ready

This file contains all 14 queries for the IC/MCS Case Risk Dashboard. Copy each query and paste into Azure Data Explorer.

## Data Source Connection

**Primary (CXE Data):**
- Cluster: `https://cxedataplatformcluster.westus2.kusto.windows.net`
- Database: `cxedata`

**Secondary (ICM Data) - for queries marked with 🔄:**
- Cluster: `https://icmcluster.kusto.windows.net`
- Database: `IcmDataWarehouse`

---

## Query 1: Summary Card
**Visual Type:** Stat/Card  
**Size:** 4×2  
**Position:** Top-left  
**Title:** 📊 Case Summary

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen >= 20
| summarize TotalCases = count(), 
            AvgRisk = round(avg(DaysOpen), 1),
            CustomersCount = dcount(TopParentName)
| project TotalCases, CustomersCount, AvgAge = AvgRisk
| extend Display = strcat("Total Cases: ", TotalCases, "\nCustomers: ", CustomersCount, "\nAvg Age: ", AvgAge, " days")
| project Display
```

---

## Query 2: Critical Count (RED ALERT)
**Visual Type:** Stat/Card  
**Size:** 2×2  
**Title:** 🚨 Critical Cases  
**Subtitle:** 90+ days old  
**Background Color:** #FFC7CE (light red)

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen > 90
| summarize CriticalCount = count()
| project CriticalCount
```

---

## Query 3: High Risk Count (YELLOW WARNING)
**Visual Type:** Stat/Card  
**Size:** 2×2  
**Title:** ⚠️ High Risk Cases  
**Subtitle:** 60-90 days  
**Background Color:** #FFF2CC (light yellow)

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen >= 60 and DaysOpen <= 90
| where OwnershipCount >= 5 or TransferCount >= 4
| summarize HighCount = count()
| project HighCount
```

---

## Query 4: Average Risk Score
**Visual Type:** Stat/Card  
**Size:** 2×2  
**Title:** Avg Risk Score

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen >= 20
| extend AgeScore = case(
    DaysOpen > 180, 56,
    DaysOpen > 120, 49,
    DaysOpen > 90, 42,
    DaysOpen > 60, 35,
    DaysOpen > 30, 28,
    DaysOpen >= 20, 14,
    0)
| extend OwnershipScore = min(OwnershipCount * 2, 20)
| extend TransferScore = min(TransferCount * 3, 15)
| extend RiskScore = AgeScore + OwnershipScore + TransferScore
| summarize AvgRisk = round(avg(RiskScore), 1)
| project AvgRisk
```

---

## Query 5: Average Age
**Visual Type:** Stat/Card  
**Size:** 2×2  
**Title:** Avg Age (days)

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen >= 20
| summarize AvgAge = round(avg(DaysOpen), 1)
| project AvgAge
```

---

## Query 6: Risk Distribution Pie Chart
**Visual Type:** Pie Chart  
**Size:** 4×4  
**Title:** Risk Level Distribution

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen >= 20
| extend RiskLevel = case(
    DaysOpen > 90, "Critical",
    DaysOpen > 60 and (OwnershipCount >= 5 or TransferCount >= 4), "High",
    DaysOpen > 40, "Medium",
    "Low")
| summarize Count = count() by RiskLevel
| order by case(RiskLevel == "Critical", 1, RiskLevel == "High", 2, RiskLevel == "Medium", 3, 4) asc
```

---

## Query 7: Age Distribution Column Chart
**Visual Type:** Column Chart  
**Size:** 4×4  
**Title:** Case Age Distribution

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen >= 20
| extend AgeBucket = case(
    DaysOpen > 180, "180+ days",
    DaysOpen > 120, "121-180 days",
    DaysOpen > 90, "91-120 days",
    DaysOpen > 60, "61-90 days",
    DaysOpen > 30, "31-60 days",
    "20-30 days")
| summarize Count = count() by AgeBucket
| order by case(
    AgeBucket == "180+ days", 1,
    AgeBucket == "121-180 days", 2,
    AgeBucket == "91-120 days", 3,
    AgeBucket == "61-90 days", 4,
    AgeBucket == "31-60 days", 5,
    6) asc
```

---

## Query 8: Top Customers Bar Chart
**Visual Type:** Bar Chart (horizontal)  
**Size:** 4×4  
**Title:** Top 10 Customers by Risk

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen >= 20
| extend AgeScore = case(
    DaysOpen > 180, 56,
    DaysOpen > 120, 49,
    DaysOpen > 90, 42,
    DaysOpen > 60, 35,
    DaysOpen > 30, 28,
    DaysOpen >= 20, 14,
    0)
| extend OwnershipScore = min(OwnershipCount * 2, 20)
| extend TransferScore = min(TransferCount * 3, 15)
| extend RiskScore = AgeScore + OwnershipScore + TransferScore
| summarize MaxRisk = max(RiskScore), CaseCount = count() by TopParentName
| top 10 by MaxRisk desc
| project Customer = TopParentName, MaxRisk, CaseCount
```

---

## Query 9: ICM Status Donut Chart 🔄
**Visual Type:** Donut Chart  
**Size:** 3×4  
**Title:** ICM Status Breakdown  
**⚠️ IMPORTANT:** Change data source to ICM cluster for this tile!

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
let ICMIds = cluster('cxedataplatformcluster.westus2.kusto.windows.net').database('cxedata').GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| where isnotempty(RelatedICM_Id)
| extend ICMList = split(RelatedICM_Id, ",")
| mv-expand ICMId = ICMList to typeof(long)
| distinct ICMId;
Incidents
| where IncidentId in (ICMIds)
| summarize arg_max(ModifiedDate, Status) by IncidentId
| summarize Count = count() by Status
| order by case(Status == "ACTIVE", 1, Status == "MITIGATED", 2, Status == "RESOLVED", 3, 4) asc
```

---

## Query 10: Risk Trend Line Chart
**Visual Type:** Time Chart / Line Chart  
**Size:** 5×4  
**Title:** 30-Day Risk Trend

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
range Date from ago(30d) to now() step 1d
| extend DummyKey = 1
| join kind=inner (
    GetSCIMIncidentV2
    | where ServiceRequestState != "Closed"
    | where ProductName == "Microsoft Purview Compliance"
    | join kind=inner ICTenants on TenantId
    | extend DummyKey = 1
) on DummyKey
| extend DaysOpenAtDate = todouble(datetime_diff('day', Date, CreatedTime))
| where DaysOpenAtDate >= 20
| extend AgeScore = case(
    DaysOpenAtDate > 180, 56,
    DaysOpenAtDate > 120, 49,
    DaysOpenAtDate > 90, 42,
    DaysOpenAtDate > 60, 35,
    DaysOpenAtDate > 30, 28,
    DaysOpenAtDate >= 20, 14,
    0)
| extend OwnershipScore = min(OwnershipCount * 2, 20)
| extend TransferScore = min(TransferCount * 3, 15)
| extend RiskScore = AgeScore + OwnershipScore + TransferScore
| summarize AvgRisk = round(avg(RiskScore), 1) by Date = startofday(Date)
| order by Date asc
```

---

## Query 11: Unassigned ICMs Card 🔄
**Visual Type:** Stat/Card  
**Size:** 2×2  
**Title:** ⚠️ Unassigned ICMs  
**Background Color:** #FFC7CE (light red)  
**⚠️ IMPORTANT:** Change data source to ICM cluster for this tile!

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
let ICMIds = cluster('cxedataplatformcluster.westus2.kusto.windows.net').database('cxedata').GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| where isnotempty(RelatedICM_Id)
| extend ICMList = split(RelatedICM_Id, ",")
| mv-expand ICMId = ICMList to typeof(long)
| distinct ICMId;
Incidents
| where IncidentId in (ICMIds)
| summarize arg_max(ModifiedDate, *) by IncidentId
| where Status == "ACTIVE"
| where isempty(OwningContactAlias) or OwningContactAlias == ""
| summarize UnassignedCount = count()
| project UnassignedCount
```

---

## Query 12: Cases with Linked Bugs 🔄
**Visual Type:** Stat/Card  
**Size:** 2×2  
**Title:** 🐛 Cases with Bugs  
**⚠️ IMPORTANT:** Change data source to ICM cluster for this tile!

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
let ICMIds = cluster('cxedataplatformcluster.westus2.kusto.windows.net').database('cxedata').GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| where isnotempty(RelatedICM_Id)
| extend ICMList = split(RelatedICM_Id, ",")
| mv-expand ICMId = ICMList to typeof(long)
| distinct ICMId;
IncidentBugs
| where IncidentId in (ICMIds)
| where IsTombstoned == false
| distinct IncidentId
| summarize BugCount = count()
| project BugCount
```

---

## Query 13: Critical Cases Table
**Visual Type:** Table  
**Size:** 12×6 (full width)  
**Title:** 🚨 Critical Cases (90+ days)

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen > 90
| extend AgeScore = case(
    DaysOpen > 180, 56,
    DaysOpen > 120, 49,
    DaysOpen > 90, 42,
    DaysOpen > 60, 35,
    DaysOpen > 30, 28,
    DaysOpen >= 20, 14,
    0)
| extend OwnershipScore = min(OwnershipCount * 2, 20)
| extend TransferScore = min(TransferCount * 3, 15)
| extend IdleScore = min(datetime_diff('day', now(), ModifiedDate) / 7 * 3, 15)
| extend ReopenScore = min(ReopenCount * 5, 10)
| extend ICMScore = iff(isnotempty(RelatedICM_Id), 10, 0)
| extend SevScore = case(ServiceRequestCurrentSeverity == "A", 5, ServiceRequestCurrentSeverity == "B", 3, 0)
| extend CritSitBonus = iff(IsCritSit == true, 10, 0)
| extend RiskScore = AgeScore + OwnershipScore + TransferScore + IdleScore + ReopenScore + ICMScore + SevScore + CritSitBonus
| extend ICMCount = iff(isnotempty(RelatedICM_Id), array_length(split(RelatedICM_Id, ",")), 0)
| extend CaseId = extract(@"id=([a-f0-9\-]+)", 1, CaseUri)
| project ServiceRequestNumber, TopParentName, DaysOpen, RiskScore, 
          AgentAlias, ManagerEmail, ServiceRequestStatus, PHE, CLE,
          ICMCount, IsCritSit, CaseId
| order by RiskScore desc, DaysOpen desc
```

---

## Query 14: All Cases Table
**Visual Type:** Table  
**Size:** 12×8 (full width, taller)  
**Title:** 📋 All IC Cases

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen >= 20
| extend AgeScore = case(
    DaysOpen > 180, 56,
    DaysOpen > 120, 49,
    DaysOpen > 90, 42,
    DaysOpen > 60, 35,
    DaysOpen > 30, 28,
    DaysOpen >= 20, 14,
    0)
| extend OwnershipScore = min(OwnershipCount * 2, 20)
| extend TransferScore = min(TransferCount * 3, 15)
| extend IdleScore = min(datetime_diff('day', now(), ModifiedDate) / 7 * 3, 15)
| extend ReopenScore = min(ReopenCount * 5, 10)
| extend ICMScore = iff(isnotempty(RelatedICM_Id), 10, 0)
| extend SevScore = case(ServiceRequestCurrentSeverity == "A", 5, ServiceRequestCurrentSeverity == "B", 3, 0)
| extend CritSitBonus = iff(IsCritSit == true, 10, 0)
| extend RiskScore = AgeScore + OwnershipScore + TransferScore + IdleScore + ReopenScore + ICMScore + SevScore + CritSitBonus
| extend RiskLevel = case(
    DaysOpen > 90, "Critical",
    RiskScore >= 60, "High",
    RiskScore >= 40, "Medium",
    "Low")
| extend HasICM = iff(isnotempty(RelatedICM_Id), "Yes", "No")
| extend CaseId = extract(@"id=([a-f0-9\-]+)", 1, CaseUri)
| project ServiceRequestNumber, TopParentName, RiskLevel, RiskScore, DaysOpen,
          AgentAlias, ServiceRequestStatus, HasICM, PHE, CLE, CaseId
| order by RiskScore desc, DaysOpen desc
```

---

## 🎯 Quick Build Instructions

1. **Create dashboard** in Azure Data Explorer
2. **Add data sources:**
   - CXE: `cxedataplatformcluster.westus2.kusto.windows.net/cxedata`
   - ICM: `icmcluster.kusto.windows.net/IcmDataWarehouse`
3. **For each query above:**
   - Copy query
   - Run in Data Explorer
   - Click "Pin to dashboard"
   - Select visual type
   - Set title/size/color
4. **Special notes:**
   - Queries 9, 11, 12 (marked 🔄) need ICM data source
   - Queries 2, 3, 11 should have colored backgrounds
   - Tables (13, 14) should be full width

Dashboard layout:
```
Row 1: [Summary][Critical][High][AvgRisk][AvgAge]
Row 2: [RiskPie][AgeChart][TopCustomers]
Row 3: [ICMStatus][RiskTrend][Unassigned][Bugs]
Row 4: [CriticalTable - full width]
Row 5: [AllCasesTable - full width]
```

Total time: ~30 minutes
