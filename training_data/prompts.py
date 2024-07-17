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
                        "$gte": 1680307200000,
                        "$lte": 1682899199000
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

    Example 14 - Give me the total count of orders for may 2023.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1682899200000,
                        "$lte": 1685577599000
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
                        "$gte": 1685577600000,
                        "$lte": 1688169599000
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
                        "$gte": 1704067200000,
                        "$lte": 1706745599000
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
                        "$gte": 1706745600000,
                        "$lte": 1709251199000
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
                        "$gte": 1709251200000,
                        "$lte": 1711929599000
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
                        "$gte": 1711929600000,
                        "$lte": 1714521599000
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
                        "$gte": 1714521600000,
                        "$lte": 1717196400000
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
                        "$lte": 1719791999000
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

    Example 21.1 - what is the order count in june 2024.
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1717200000000,
                        "$lte": 1719791999000
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
                        "$gte": 1719792000000,
                        "$lte": 1722470399000
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
                    "$lte": 1719791999000
                    }
                }
           },
        {
            "$group": {
                "_id": null,
                "count": {
                    "$sum": "$Price"
                    }
                }
            }
        ]
   }

    Example 25 - What is the revenue for past 6 months?
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "ScheduledDate": {
                        "$gte": 1704067200000,
                        "$lte": 1719791999000
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


    Example 27 - What is the revenue generated from Renje Ramesan for last month?
    The MongoDB command will be like this: {
        "aggregate": [
            {
                "$match": {
                    "SalesPerson.name": {"$regex": ".*Renje Ramesan.*", "$options": "i"},
                    "ScheduledDate": {
                        "$gte": 1717200000000,
                        "$lte": 1719791999000
                    }
                }
            },
            {
                "$group": {
                    "_id": null,
                    "count": {
                        "$sum": "$Price"
                    }
                }
            }
        ]
    }

    Example 28 - what is the largest order in june 2024?
    The MongoDB command will be like this: {
           "aggregate": [
            {
               "$match": {
                "ScheduledDate": {
                    "$gte": 1717200000000,
                    "$lte": 1719791999000
                }
            }
        },
        {
            "$group": {
                "_id": null,
                "count": {
                    "$max": "$Price"
                    }
                }
            }
        ]
    }

    Example 29 - Give me the price of customer star cement co LLC ?
    The MongoDB command will be like this: {
        "aggregate": [
            { "$match": {"UserDetails.fullName": {"$regex": ".*star cement co LLC.*", "$options": "i"}}},
            { "$group": {"_id": "$UserDetails.fullName", "customerwisePrice": { "$sum": "$Price" }}}
        ]
    }

    Example 30 - price of star cement co LLC ?
    The MongoDB command will be like this: {
        "aggregate": [
            { "$match": {"UserDetails.fullName": {"$regex": ".*star cement co LLC.*", "$options": "i"}}},
            { "$group": {"_id": "$UserDetails.fullName", "customerwisePrice": { "$sum": "$Price" }}}
        ]
    }

    Example 31 - revenue of star cement co LLC ?
    The MongoDB command will be like this: {
        "aggregate": [
            { "$match": {"UserDetails.fullName": {"$regex": ".*star cement co LLC.*", "$options": "i"}}},
            { "$group": {"_id": "$UserDetails.fullName", "customerwisePrice": { "$sum": "$Price" }}}
        ]
    }

    
    Example 32 - "revenue of star cement co LLC in may 2024"
    The MongoDB command will be like this: {
    "aggregate": [
        {
            "$match": {
                "UserDetails.fullName": {"$regex": ".*star cement co LLC.*", "$options": "i"},
                "ScheduledDate": {
                    "$gte": 1714521600000,
                    "$lte": 1717196400000
                }
            }
        },
         { "$group": {"_id": "$UserDetails.fullName", "customerwisePrice": { "$sum": "$Price" }}}
        ]
    }

    Example 33 - Give me the profit in June 2024?
    The MongoDB command will be like this: {
    "aggregate": [
        {
            "$match": {
                "ScheduledDate": {
                    "$gte": 1717200000000,
                    "$lte": 1719791999000
                }
            }
        },
        {
            "$group": {
                "_id": null,
                "total_price": {
                    "$sum": "$Price"
                },
                "total_hauler_price": {
                    "$sum": "$HaulerPrice"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "ProfitData": {
                    "Price": "$total_price",
                    "Hauler Price": "$total_hauler_price",
                    "Profit": {
                        "$subtract": ["$total_price", "$total_hauler_price"]
                       }
                    }
                }
            }
        ]
    }


    Example 34 - Give me the profit in 2024?
    The MongoDB command will be like this: {
    "aggregate": [
        {
            "$match": {
                "ScheduledDate": {
                    "$gte": 1704067200000,
                    "$lte": 1735689599000
                }
            }
        },
        {
            "$group": {
                "_id": null,
                "total_price": {
                    "$sum": "$Price"
                },
                "total_hauler_price": {
                    "$sum": "$HaulerPrice"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "ProfitData": {
                    "Price": "$total_price",
                    "Hauler Price": "$total_hauler_price",
                    "Profit": {
                        "$subtract": ["$total_price", "$total_hauler_price"]
                    }
                }
            }
        }
    ]
}


    Example 35 - Give me the profit of Star cement co LLC in June 2024?
    The MongoDB command will be like this: {
    "aggregate": [
        {
            "$match": {
                "ScheduledDate": {
                    "$gte": 1717200000000,
                    "$lte": 1719791999000
                },
                "UserDetails.fullName": {
                    "$regex": "Star cement co LLC",
                    "$options": "i"
                }
            }
        },
        {
            "$group": {
                "_id": null,
                "total_price": {
                    "$sum": "$Price"
                },
                "total_hauler_price": {
                    "$sum": "$HaulerPrice"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "ProfitData": {
                    "Price": "$total_price",
                    "Hauler Price": "$total_hauler_price",
                    "Profit": {
                        "$subtract": ["$total_price", "$total_hauler_price"]
                    }
                }
            }
        }
    ]
}


    Example 36 - Give me the profit of first quarter in 2024?
    The MongoDB command will be like this: {
    "aggregate": [
        {
            "$match": {
                "ScheduledDate": {
                    "$gte": 1704067200000,
                    "$lte": 1711929599000
                }
            }
        },
        {
            "$group": {
                "_id": null,
                "total_price": {
                    "$sum": "$Price"
                },
                "total_hauler_price": {
                    "$sum": "$HaulerPrice"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "ProfitData": {
                    "Price": "$total_price",
                    "Hauler Price": "$total_hauler_price",
                    "Profit": {
                        "$subtract": ["$total_price", "$total_hauler_price"]
                       }
                    }
                }
            }
        ]
    }

    Example 37 - Give me the profit of second quarter in 2024?
    The MongoDB command will be like this: {
    "aggregate": [
        {
            "$match": {
                "ScheduledDate": {
                    "$gte": 1711929600000,
                    "$lte": 1719791999000
                }
            }
        },
        {
            "$group": {
                "_id": null,
                "total_price": {
                    "$sum": "$Price"
                },
                "total_hauler_price": {
                    "$sum": "$HaulerPrice"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "ProfitData": {
                    "Price": "$total_price",
                    "Hauler Price": "$total_hauler_price",
                    "Profit": {
                        "$subtract": ["$total_price", "$total_hauler_price"]
                       }
                    }
                }
            }
        ]
    }

    Example 38 - Give me the profit of third quarter in 2024?
    The MongoDB command will be like this: {
    "aggregate": [
        {
            "$match": {
                "ScheduledDate": {
                    "$gte": 1719792000000,
                    "$lte": 1727654399000
                }
            }
        },
        {
            "$group": {
                "_id": null,
                "total_price": {
                    "$sum": "$Price"
                },
                "total_hauler_price": {
                    "$sum": "$HaulerPrice"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "ProfitData": {
                    "Price": "$total_price",
                    "Hauler Price": "$total_hauler_price",
                    "Profit": {
                        "$subtract": ["$total_price", "$total_hauler_price"]
                    }
                }
            }
        }
    ]
}

    Example 38 - Give me the profit of fourth quarter in 2024?
    The MongoDB command will be like this: {
    "aggregate": [
        {
            "$match": {
                "ScheduledDate": {
                    "$gte": 1727740800000,
                    "$lte": 1735689599000
                }
            }
        },
        {
            "$group": {
                "_id": null,
                "total_price": {
                    "$sum": "$Price"
                },
                "total_hauler_price": {
                    "$sum": "$HaulerPrice"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "ProfitData": {
                    "Price": "$total_price",
                    "Hauler Price": "$total_hauler_price",
                    "Profit": {
                        "$subtract": ["$total_price", "$total_hauler_price"]
                    }
                }
            }
        }
    ]
}





    



    The query code should be a valid MongoDB query in JSON format.
    """
]

