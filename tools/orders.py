"""
Order and Transaction History Tools
Retrieves order details, transaction history, and fulfillment status.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

# Sample order data for PoC
_sample_orders: Dict[str, Dict[str, Any]] = {
    "ORD001": {
        "order_id": "ORD001",
        "customer_id": "CUST001",
        "order_date": "2025-01-15T10:30:00Z",
        "status": "delivered",
        "total_amount": 149.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM001",
                "product_name": "Wireless Headphones",
                "quantity": 1,
                "price": 99.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            },
            {
                "item_id": "ITEM002",
                "product_name": "USB-C Cable",
                "quantity": 2,
                "price": 25.00,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        },
        "payment_method": "card",
        "last_four": "4532"
    },
    "ORD002": {
        "order_id": "ORD002",
        "customer_id": "CUST001",
        "order_date": "2025-02-01T14:20:00Z",
        "status": "delivered",
        "total_amount": 79.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM003",
                "product_name": "Phone Case",
                "quantity": 1,
                "price": 79.99,
                "condition": "used",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        },
        "payment_method": "card",
        "last_four": "4532"
    },
    "ORD003": {
        "order_id": "ORD003",
        "customer_id": "CUST002",
        "order_date": "2025-01-20T09:15:00Z",
        "status": "delivered",
        "total_amount": 299.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM004",
                "product_name": "Smart Watch",
                "quantity": 1,
                "price": 299.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "456 Oak Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90001"
        },
        "payment_method": "card",
        "last_four": "7891"
    },
    "ORD004": {
        "order_id": "ORD004",
        "customer_id": "CUST001",
        "order_date": "2025-02-10T11:45:00Z",
        "status": "delivered",
        "total_amount": 199.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM005",
                "product_name": "Bluetooth Speaker",
                "quantity": 1,
                "price": 199.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        },
        "payment_method": "card",
        "last_four": "4532"
    },
    "ORD005": {
        "order_id": "ORD005",
        "customer_id": "CUST002",
        "order_date": "2025-01-25T16:30:00Z",
        "status": "delivered",
        "total_amount": 89.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM006",
                "product_name": "Wireless Mouse",
                "quantity": 1,
                "price": 89.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "456 Oak Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90001"
        },
        "payment_method": "card",
        "last_four": "7891"
    },
    "ORD006": {
        "order_id": "ORD006",
        "customer_id": "CUST003",
        "order_date": "2025-01-18T13:20:00Z",
        "status": "delivered",
        "total_amount": 349.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM007",
                "product_name": "Gaming Keyboard",
                "quantity": 1,
                "price": 349.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "789 Pine Street",
            "city": "Chicago",
            "state": "IL",
            "zip": "60601"
        },
        "payment_method": "card",
        "last_four": "2345"
    },
    "ORD007": {
        "order_id": "ORD007",
        "customer_id": "CUST003",
        "order_date": "2025-02-05T09:00:00Z",
        "status": "delivered",
        "total_amount": 129.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM008",
                "product_name": "Webcam HD",
                "quantity": 1,
                "price": 129.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "789 Pine Street",
            "city": "Chicago",
            "state": "IL",
            "zip": "60601"
        },
        "payment_method": "card",
        "last_four": "2345"
    },
    "ORD008": {
        "order_id": "ORD008",
        "customer_id": "CUST004",
        "order_date": "2025-01-22T15:45:00Z",
        "status": "delivered",
        "total_amount": 249.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM009",
                "product_name": "Tablet Stand",
                "quantity": 1,
                "price": 249.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "321 Elm Drive",
            "city": "Houston",
            "state": "TX",
            "zip": "77001"
        },
        "payment_method": "card",
        "last_four": "6789"
    },
    "ORD009": {
        "order_id": "ORD009",
        "customer_id": "CUST005",
        "order_date": "2025-01-12T08:30:00Z",
        "status": "delivered",
        "total_amount": 179.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM010",
                "product_name": "Portable Charger",
                "quantity": 1,
                "price": 179.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "555 Maple Lane",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85001"
        },
        "payment_method": "card",
        "last_four": "1234"
    },
    "ORD010": {
        "order_id": "ORD010",
        "customer_id": "CUST005",
        "order_date": "2025-01-28T12:15:00Z",
        "status": "delivered",
        "total_amount": 59.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM011",
                "product_name": "Screen Protector",
                "quantity": 2,
                "price": 29.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "555 Maple Lane",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85001"
        },
        "payment_method": "card",
        "last_four": "1234"
    },
    "ORD011": {
        "order_id": "ORD011",
        "customer_id": "CUST005",
        "order_date": "2025-02-08T10:00:00Z",
        "status": "delivered",
        "total_amount": 399.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM012",
                "product_name": "Noise Cancelling Earbuds",
                "quantity": 1,
                "price": 399.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "555 Maple Lane",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85001"
        },
        "payment_method": "card",
        "last_four": "1234"
    },
    "ORD012": {
        "order_id": "ORD012",
        "customer_id": "CUST006",
        "order_date": "2025-01-30T14:30:00Z",
        "status": "delivered",
        "total_amount": 159.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM013",
                "product_name": "USB Hub",
                "quantity": 1,
                "price": 159.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "888 Cedar Boulevard",
            "city": "Miami",
            "state": "FL",
            "zip": "33101"
        },
        "payment_method": "card",
        "last_four": "5678"
    },
    "ORD013": {
        "order_id": "ORD013",
        "customer_id": "CUST007",
        "order_date": "2025-02-03T11:20:00Z",
        "status": "delivered",
        "total_amount": 219.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM014",
                "product_name": "External Hard Drive",
                "quantity": 1,
                "price": 219.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "222 Birch Court",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101"
        },
        "payment_method": "card",
        "last_four": "9012"
    },
    "ORD014": {
        "order_id": "ORD014",
        "customer_id": "CUST007",
        "order_date": "2025-02-12T09:45:00Z",
        "status": "delivered",
        "total_amount": 69.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM015",
                "product_name": "Laptop Sleeve",
                "quantity": 1,
                "price": 69.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "222 Birch Court",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101"
        },
        "payment_method": "card",
        "last_four": "9012"
    },
    "ORD015": {
        "order_id": "ORD015",
        "customer_id": "CUST008",
        "order_date": "2025-01-26T17:00:00Z",
        "status": "delivered",
        "total_amount": 279.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM016",
                "product_name": "Monitor Stand",
                "quantity": 1,
                "price": 279.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "444 Spruce Avenue",
            "city": "Boston",
            "state": "MA",
            "zip": "02101"
        },
        "payment_method": "card",
        "last_four": "3456"
    },
    "ORD016": {
        "order_id": "ORD016",
        "customer_id": "CUST009",
        "order_date": "2025-02-05T14:30:00Z",
        "status": "delivered",
        "total_amount": 189.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM017",
                "product_name": "Mechanical Keyboard",
                "quantity": 1,
                "price": 189.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "777 Willow Way",
            "city": "Denver",
            "state": "CO",
            "zip": "80201"
        },
        "payment_method": "card",
        "last_four": "4567"
    },
    "ORD017": {
        "order_id": "ORD017",
        "customer_id": "CUST009",
        "order_date": "2025-11-08T10:15:00Z",
        "status": "delivered",
        "total_amount": 119.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM018",
                "product_name": "Wireless Charging Pad",
                "quantity": 1,
                "price": 119.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "777 Willow Way",
            "city": "Denver",
            "state": "CO",
            "zip": "80201"
        },
        "payment_method": "card",
        "last_four": "4567"
    },
    "ORD018": {
        "order_id": "ORD018",
        "customer_id": "CUST010",
        "order_date": "2025-02-03T16:45:00Z",
        "status": "delivered",
        "total_amount": 259.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM019",
                "product_name": "Smart Home Hub",
                "quantity": 1,
                "price": 259.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "999 River Road",
            "city": "Portland",
            "state": "OR",
            "zip": "97201"
        },
        "payment_method": "card",
        "last_four": "8901"
    },
    "ORD019": {
        "order_id": "ORD019",
        "customer_id": "CUST011",
        "order_date": "2025-02-06T11:20:00Z",
        "status": "delivered",
        "total_amount": 139.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM020",
                "product_name": "USB-C Dock",
                "quantity": 1,
                "price": 139.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "111 Forest Avenue",
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        },
        "payment_method": "card",
        "last_four": "2345"
    },
    "ORD020": {
        "order_id": "ORD020",
        "customer_id": "CUST011",
        "order_date": "2025-02-10T09:30:00Z",
        "status": "delivered",
        "total_amount": 89.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM021",
                "product_name": "Laptop Stand Adjustable",
                "quantity": 1,
                "price": 89.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "111 Forest Avenue",
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        },
        "payment_method": "card",
        "last_four": "2345"
    },
    "ORD021": {
        "order_id": "ORD021",
        "customer_id": "CUST012",
        "order_date": "2025-02-07T13:00:00Z",
        "status": "delivered",
        "total_amount": 329.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM022",
                "product_name": "4K Webcam",
                "quantity": 1,
                "price": 329.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "333 Ocean Drive",
            "city": "San Diego",
            "state": "CA",
            "zip": "92101"
        },
        "payment_method": "card",
        "last_four": "6789"
    },
    "ORD022": {
        "order_id": "ORD022",
        "customer_id": "CUST013",
        "order_date": "2025-02-09T15:20:00Z",
        "status": "delivered",
        "total_amount": 199.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM023",
                "product_name": "Ergonomic Mouse",
                "quantity": 1,
                "price": 199.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "666 Mountain View",
            "city": "Nashville",
            "state": "TN",
            "zip": "37201"
        },
        "payment_method": "card",
        "last_four": "0123"
    },
    "ORD023": {
        "order_id": "ORD023",
        "customer_id": "CUST014",
        "order_date": "2025-02-04T12:10:00Z",
        "status": "delivered",
        "total_amount": 149.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM024",
                "product_name": "Wireless Earbuds Pro",
                "quantity": 1,
                "price": 149.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "222 Park Boulevard",
            "city": "Minneapolis",
            "state": "MN",
            "zip": "55401"
        },
        "payment_method": "card",
        "last_four": "7890"
    },
    "ORD024": {
        "order_id": "ORD024",
        "customer_id": "CUST014",
        "order_date": "2025-02-11T08:45:00Z",
        "status": "delivered",
        "total_amount": 79.99,
        "currency": "USD",
        "items": [
            {
                "item_id": "ITEM025",
                "product_name": "Phone Stand with Charger",
                "quantity": 1,
                "price": 79.99,
                "condition": "unopened",
                "fulfillment_status": "delivered"
            }
        ],
        "shipping_address": {
            "street": "222 Park Boulevard",
            "city": "Minneapolis",
            "state": "MN",
            "zip": "55401"
        },
        "payment_method": "card",
        "last_four": "7890"
    }
}

_sample_transactions: Dict[str, List[Dict[str, Any]]] = {
    "ORD001": [
        {
            "transaction_id": "TXN001",
            "order_id": "ORD001",
            "type": "charge",
            "amount": 149.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-15T10:30:15Z",
            "payment_method": "card",
            "last_four": "4532"
        }
    ],
    "ORD002": [
        {
            "transaction_id": "TXN002",
            "order_id": "ORD002",
            "type": "charge",
            "amount": 79.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-01T14:20:10Z",
            "payment_method": "card",
            "last_four": "4532"
        }
    ],
    "ORD003": [
        {
            "transaction_id": "TXN003",
            "order_id": "ORD003",
            "type": "charge",
            "amount": 299.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-20T09:15:20Z",
            "payment_method": "card",
            "last_four": "7891"
        }
    ],
    "ORD004": [
        {
            "transaction_id": "TXN004",
            "order_id": "ORD004",
            "type": "charge",
            "amount": 199.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-10T11:45:15Z",
            "payment_method": "card",
            "last_four": "4532"
        }
    ],
    "ORD005": [
        {
            "transaction_id": "TXN005",
            "order_id": "ORD005",
            "type": "charge",
            "amount": 89.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-25T16:30:20Z",
            "payment_method": "card",
            "last_four": "7891"
        }
    ],
    "ORD006": [
        {
            "transaction_id": "TXN006",
            "order_id": "ORD006",
            "type": "charge",
            "amount": 349.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-18T13:20:25Z",
            "payment_method": "card",
            "last_four": "2345"
        }
    ],
    "ORD007": [
        {
            "transaction_id": "TXN007",
            "order_id": "ORD007",
            "type": "charge",
            "amount": 129.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-05T09:00:30Z",
            "payment_method": "card",
            "last_four": "2345"
        }
    ],
    "ORD008": [
        {
            "transaction_id": "TXN008",
            "order_id": "ORD008",
            "type": "charge",
            "amount": 249.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-22T15:45:35Z",
            "payment_method": "card",
            "last_four": "6789"
        }
    ],
    "ORD009": [
        {
            "transaction_id": "TXN009",
            "order_id": "ORD009",
            "type": "charge",
            "amount": 179.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-12T08:30:40Z",
            "payment_method": "card",
            "last_four": "1234"
        }
    ],
    "ORD010": [
        {
            "transaction_id": "TXN010",
            "order_id": "ORD010",
            "type": "charge",
            "amount": 59.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-28T12:15:45Z",
            "payment_method": "card",
            "last_four": "1234"
        }
    ],
    "ORD011": [
        {
            "transaction_id": "TXN011",
            "order_id": "ORD011",
            "type": "charge",
            "amount": 399.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-08T10:00:50Z",
            "payment_method": "card",
            "last_four": "1234"
        }
    ],
    "ORD012": [
        {
            "transaction_id": "TXN012",
            "order_id": "ORD012",
            "type": "charge",
            "amount": 159.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-30T14:30:55Z",
            "payment_method": "card",
            "last_four": "5678"
        }
    ],
    "ORD013": [
        {
            "transaction_id": "TXN013",
            "order_id": "ORD013",
            "type": "charge",
            "amount": 219.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-03T11:20:05Z",
            "payment_method": "card",
            "last_four": "9012"
        }
    ],
    "ORD014": [
        {
            "transaction_id": "TXN014",
            "order_id": "ORD014",
            "type": "charge",
            "amount": 69.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-12T09:45:10Z",
            "payment_method": "card",
            "last_four": "9012"
        }
    ],
    "ORD015": [
        {
            "transaction_id": "TXN015",
            "order_id": "ORD015",
            "type": "charge",
            "amount": 279.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-01-26T17:00:15Z",
            "payment_method": "card",
            "last_four": "3456"
        }
    ],
    "ORD016": [
        {
            "transaction_id": "TXN016",
            "order_id": "ORD016",
            "type": "charge",
            "amount": 189.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-05T14:30:20Z",
            "payment_method": "card",
            "last_four": "4567"
        }
    ],
    "ORD017": [
        {
            "transaction_id": "TXN017",
            "order_id": "ORD017",
            "type": "charge",
            "amount": 119.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-11-08T10:15:25Z",
            "payment_method": "card",
            "last_four": "4567"
        }
    ],
    "ORD018": [
        {
            "transaction_id": "TXN018",
            "order_id": "ORD018",
            "type": "charge",
            "amount": 259.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-03T16:45:30Z",
            "payment_method": "card",
            "last_four": "8901"
        }
    ],
    "ORD019": [
        {
            "transaction_id": "TXN019",
            "order_id": "ORD019",
            "type": "charge",
            "amount": 139.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-06T11:20:35Z",
            "payment_method": "card",
            "last_four": "2345"
        }
    ],
    "ORD020": [
        {
            "transaction_id": "TXN020",
            "order_id": "ORD020",
            "type": "charge",
            "amount": 89.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-10T09:30:40Z",
            "payment_method": "card",
            "last_four": "2345"
        }
    ],
    "ORD021": [
        {
            "transaction_id": "TXN021",
            "order_id": "ORD021",
            "type": "charge",
            "amount": 329.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-07T13:00:45Z",
            "payment_method": "card",
            "last_four": "6789"
        }
    ],
    "ORD022": [
        {
            "transaction_id": "TXN022",
            "order_id": "ORD022",
            "type": "charge",
            "amount": 199.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-09T15:20:50Z",
            "payment_method": "card",
            "last_four": "0123"
        }
    ],
    "ORD023": [
        {
            "transaction_id": "TXN023",
            "order_id": "ORD023",
            "type": "charge",
            "amount": 149.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-04T12:10:55Z",
            "payment_method": "card",
            "last_four": "7890"
        }
    ],
    "ORD024": [
        {
            "transaction_id": "TXN024",
            "order_id": "ORD024",
            "type": "charge",
            "amount": 79.99,
            "currency": "USD",
            "status": "completed",
            "timestamp": "2025-02-11T08:45:05Z",
            "payment_method": "card",
            "last_four": "7890"
        }
    ]
}


class OrderHistoryService:
    """Handles order and transaction history retrieval."""
    
    async def get_order_history(
        self,
        customer_id: str,
        order_id: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Retrieve order history for a customer.
        
        Args:
            customer_id: Verified customer ID
            order_id: Specific order ID (optional) - accepts both ORD-001 and ORD001 formats
            limit: Maximum number of orders to return
        
        Returns:
            Dict with orders list and metadata
        """
        # Normalize customer_id (remove hyphens)
        normalized_customer_id = customer_id.replace("-", "")
        
        # Filter orders by customer
        customer_orders = [
            order for order in _sample_orders.values()
            if order["customer_id"] == normalized_customer_id or order["customer_id"] == customer_id
        ]
        
        # Filter by specific order if provided
        if order_id:
            # Normalize order_id (remove hyphens) to handle both formats
            normalized_order_id = order_id.replace("-", "")
            customer_orders = [
                order for order in customer_orders
                if order["order_id"] == normalized_order_id or order["order_id"] == order_id
            ]
        
        # Sort by date (newest first) and limit
        customer_orders.sort(
            key=lambda x: x["order_date"],
            reverse=True
        )
        customer_orders = customer_orders[:limit]
        
        return {
            "customer_id": customer_id,
            "orders": customer_orders,
            "total_count": len(customer_orders),
            "retrieved_at": datetime.utcnow().isoformat() + "Z"
        }
    
    async def get_transaction_history(
        self,
        order_id: str,
        customer_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve transaction/payment history for a specific order.
        
        Args:
            order_id: Order ID - accepts both ORD-001 and ORD001 formats
            customer_id: Verified customer ID (for authorization check) - accepts both CUST-001 and CUST001 formats
        
        Returns:
            Dict with transactions list
        """
        # Normalize IDs (remove hyphens) to handle both formats
        normalized_order_id = order_id.replace("-", "")
        normalized_customer_id = customer_id.replace("-", "")
        
        # Try to find order with normalized ID first, then original
        order = _sample_orders.get(normalized_order_id) or _sample_orders.get(order_id)
        
        if not order:
            return {
                "error": "Order not found",
                "order_id": order_id
            }
        
        # Check customer match (normalized or original)
        order_customer_id = order["customer_id"]
        if order_customer_id != normalized_customer_id and order_customer_id != customer_id:
            return {
                "error": "Unauthorized: Order does not belong to customer",
                "order_id": order_id
            }
        
        # Get transactions for this order (try normalized ID first, then original)
        transactions = _sample_transactions.get(normalized_order_id, []) or _sample_transactions.get(order_id, [])
        
        return {
            "order_id": normalized_order_id,  # Return normalized format
            "customer_id": customer_id,
            "transactions": transactions,
            "total_count": len(transactions),
            "retrieved_at": datetime.utcnow().isoformat() + "Z"
        }


