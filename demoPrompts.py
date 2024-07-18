#     Example 35.1 - Give me the profit of first quarter in 2023?
#     The MongoDB command will be like this: {
#     "aggregate": [
#         {
#             "$match": {
#                 "ScheduledDate": {
#                     "$gte": 1672531200000,
#                     "$lte": 1680307199000
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": null,
#                 "total_price": {
#                     "$sum": "$Price"
#                 },
#                 "total_hauler_price": {
#                     "$sum": "$HaulerPrice"
#                 }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "ProfitData": {
#                     "Price": "$total_price",
#                     "Hauler Price": "$total_hauler_price",
#                     "Profit": {
#                         "$subtract": ["$total_price", "$total_hauler_price"]
#                     }
#                 }
#             }
#         }
#     ]
# }

#     Example 35.2 - Give me the profit of second quarter in 2023?
#     The MongoDB command will be like this: {
#     "aggregate": [
#         {
#             "$match": {
#                 "ScheduledDate": {
#                     "$gte": 1680220800000,
#                     "$lte": 1688169599000
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": null,
#                 "total_price": {
#                     "$sum": "$Price"
#                 },
#                 "total_hauler_price": {
#                     "$sum": "$HaulerPrice"
#                 }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "ProfitData": {
#                     "Price": "$total_price",
#                     "Hauler Price": "$total_hauler_price",
#                     "Profit": {
#                         "$subtract": ["$total_price", "$total_hauler_price"]
#                     }
#                 }
#             }
#         }
#     ]
# }

#     Example 35.3 - Give me the profit of third quarter in 2023?
#     The MongoDB command will be like this: {
#     "aggregate": [
#         {
#             "$match": {
#                 "ScheduledDate": {
#                     "$gte": 1672531200000,
#                     "$lte": 1696204799000
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": null,
#                 "total_price": {
#                     "$sum": "$Price"
#                 },
#                 "total_hauler_price": {
#                     "$sum": "$HaulerPrice"
#                 }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "ProfitData": {
#                     "Price": "$total_price",
#                     "Hauler Price": "$total_hauler_price",
#                     "Profit": {
#                         "$subtract": ["$total_price", "$total_hauler_price"]
#                     }
#                 }
#             }
#         }
#     ]
# }


#     Example 35.3 - Give me the profit of fourth quarter in 2023?
#     The MongoDB command will be like this: {
#     "aggregate": [
#         {
#             "$match": {
#                 "ScheduledDate": {
#                     "$gte": 1696118400000,
#                     "$lte": 1735689599000
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": null,
#                 "total_price": {
#                     "$sum": "$Price"
#                 },
#                 "total_hauler_price": {
#                     "$sum": "$HaulerPrice"
#                 }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "ProfitData": {
#                     "Price": "$total_price",
#                     "Hauler Price": "$total_hauler_price",
#                     "Profit": {
#                         "$subtract": ["$total_price", "$total_hauler_price"]
#                     }
#                 }
#             }
#         }
#     ]
# }
