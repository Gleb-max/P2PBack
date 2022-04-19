API_URL = 'https://graphql.bitquery.io/'
API_KEY = 'BQYCBzGkFOeo0eaexw9Jv4rXhLIVMfHL'

SEARCH_QUERY = """
query ($address: String!, $limit: Int!, $offset: Int!, $till: ISO8601DateTime) {
  ethereum {
    smartContractCalls(
      options: {desc: "block.timestamp.time", limit: $limit, offset: $offset}
      date: {since: "2021-03-01", till: $till}
      txHash: {is: $address}
    ) {
      block {
        timestamp {
          time(format: "%Y-%m-%d %H:%M:%S")
        }
        height
      }
      smartContractMethod {
        name
        signatureHash
      }
      smartContract {
        contractType
      }
      address: caller {
        address
        annotation
      }
      transaction {
        hash        
      }
      gasValue
      external
    }
  }
}
"""
