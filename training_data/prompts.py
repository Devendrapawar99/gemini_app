prompt = [
    """
    You are an expert in converting English questions to MongoDB queries!
    The MongoDB collection has the name ORDERS and has the following fields:
    
    - _id
    - PK
    - UserDetails (Object)
        - phoneNumber
        - emirate
        - phone
        - rate
        - erpCode
        - fullName
        - email
    - RecordType
    - Status
    - PriceTTC
    - HaulerPrice
    - UOM
    - ScheduledDate
    - SalesPerson (Object)
        - SK
        - name
        - pk
        - phoneNumber
        - RecordType
        - email
        - Price
        - CreatedAt
    - VehicleDetails (Object)
        - HelpersNumber
        - Category
        - Description
        - InstallerNumber
        - VehicleTypeAr
        - CategoryAr
        - VehicleType
        - SK
        - PK
        - Image
        - DescriptionAr
        - Data
        - BranchId
    - Inquiry (Object)
        - SalesPrice
        - Type
        - OrderId
    - Customer (Object)
        - PK
        - BranchId
        - Email
        - Phone
        - FullName
        - TargetBuyingPrice
        - SK
        - CostPrice
        - InquiryNoOfVehicles
        - NoOfVehicles
        - HaulerPriceTTC
        - Type
        - OrderId
    - SourcePerson (Object)
        - sk
        - name
        - pk
        - phoneNumber
        - RecordType
        - email
    - Branch (Object)
        - SK
        - BranchName
        - PK
        - CompanyCode
        - Currency
    - CreatedAt
    - UpdatedAt

    
    Example 1 - Orders in Abu Dhabi?
    The MongoDB command will be like this: {"aggregate": [{"$match": {"UserDetails.emirate": "Abu Dhabi"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}

    Example 3 - Give me the Status of the order with ID "240600278-2"?
    The MongoDB command will be like this: {"filter": {"OrderId": "240600278-2"}, "fields": ["Status"]}

    Example 4 - Give me the total of all orders price?
    The MongoDB command will be like this: {"aggregate": [{"$group": {"_id": null, "count": {"$sum": "$Price"}}}]}

    Example 5 - Give me the SalesPrice of the order with ID "240600278-2"?
    The MongoDB command will be like this: {"filter": {"OrderId": "Order#1719578812822"}, "count": ["Inquiry.SalesPrice"]}

    Example 6 - Give me the CostPrice of the order with ID "240600278-2"?
    The MongoDB command will be like this: {"filter": {"OrderId": "240600278-2"}, "count": ["Inquiry.CostPrice"]}

    Example 8 - Example: Give me the count of orders managed by Salesperson joseph daniel.
    The MongoDB command will be like this: {"aggregate": [{"$match": {"SalesPerson.name": "Joseph Daniel"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}

    Example 9 - Give me the count of orders with status "pending".
    The MongoDB command will be like this: {"aggregate": [{"$match": {"Status": "pending"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}
    
    Example 10 - Give me the total enterprise orders.
    The MongoDB command will be like this: {"aggregate": [{"$match": {"Inquiry.Type": "move_enterprise"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}

    Example 11 - Give me the count of orders from the sharjah branch.
    The MongoDB command will be like this: {"aggregate": [{"$match": {"Branch.BranchName": "re.life (FZE) Sharjah"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}

    Example 12 - Count of orders which were sent cross border.
    The MongoDB command will be like this: {"aggregate": [{"$match": {"Type": "cross_border"}}, {"$group": {"_id": null, "count": {"$sum": 1}}}]}

    Example 13 - Give me the total count of orders for april 2023.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1680290400000,
                        "$lte": 1682809400000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 14 - Give me the total count of orders for june 2023.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1685639400000,
                        "$lte": 1688119400000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 15 - Give me the total count of orders for june 2023.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1685639400000,
                        "$lte": 1687999400000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 16 - Give me the total count of orders for january 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1704128000000,
                        "$lte": 1706678000000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 17 - Give me the total count of orders for february 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1706728000000,
                        "$lte": 1709205200000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 18 - Give me the total count of orders for march 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1709302000000,
                        "$lte": 1711902000000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 19 - Give me the total count of orders for april 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1711912000000,
                        "$lte": 1714460000000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 20 - Give me the total count of orders for may 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1714550000000,
                        "$lte": 1717150000000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 21 - Give me the total count of orders for june 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1717200000000,
                        "$lte": 1719771600000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 22 - Give me the total count of orders for july 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1719779200000,
                        "$lte": 1722370800000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 23 - Give me the total count of orders for august 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1722451200000,
                        "$lte": 1725043200000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }

    Example 24 - What is the revenue of last month?
    The MongoDB command will be like this: {
        "aggregate": [
           {
                "$match": {
                    "ScheduledDate": {
                    "$gte": 1717200000000,
                    "$lte": 1719771600000
                    }
                }
           },
        {
            "$group": {
                "_id": null,
                "revenue": {
                    "$sum": "$Price"
                    }
                }
            }
        ]
   }

    Example 23 - What is the revenue for past 6 months?
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1704128000000,
                        "$lte": 1719771600000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
    }



    The query code should be a valid MongoDB query in JSON format.
    """
]