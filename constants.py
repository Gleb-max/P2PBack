API_URL = 'https://graphql.bitquery.io/'
API_KEY = 'BQYCBzGkFOeo0eaexw9Jv4rXhLIVMfHL'

SEARCH_QUERY = """
query ($tx: String!) {
  ethereum(network: ethereum) {
    smartContractCalls(
      options: {asc: "callDepth"}
      txHash: {is: $tx}
    ) {
      smartContract {
        address {
          address
          annotation
        }
        contractType
        protocolType
        currency {
          symbol
        }
      }
      smartContractMethod {
        name
        signatureHash
      }
      caller {
        address
        annotation
        smartContract {
          contractType
          currency {
            symbol
        }
      }
      }
      success
      amount
      gasValue
      callDepth
    }
  }
}
"""

# SEARCH_QUERY = """
# query ($address: String!, $limit: Int!, $offset: Int!, $till: ISO8601DateTime) {
#   ethereum {
#     smartContractCalls(
#       options: {desc: "block.timestamp.time", limit: $limit, offset: $offset}
#       date: {since: "2021-03-01", till: $till}
#       txHash: {is: $address}
#     ) {
#       block {
#         timestamp {
#           time(format: "%Y-%m-%d %H:%M:%S")
#         }
#         height
#       }
#       smartContractMethod {
#         name
#         signatureHash
#       }
#       smartContract {
#         contractType
#         currency {
#           symbol
#         }
#       }
#       address: caller {
#         address
#         annotation
#       }
#       transaction {
#         hash
#       }
#       gasValue
#       external
#     }
#   }
# }
# """
