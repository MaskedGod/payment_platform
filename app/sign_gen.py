import hmac
import hashlib

from config.settings import settings


body = """{
  "id": "12345",
  "referenceId": "payment-123",
  "paymentType": "DEPOSIT",
  "state": "COMPLETED",
  "description": "Funding the account",
  "parentPaymentId": "a0981ba1540d4062bc42d4019607sf94",
  "paymentMethod": "BASIC_CARD",
  "paymentMethodDetails": {
    "customerAccountNumber": "400000***0002",
    "cardholderName": "Harry Potter",
    "cardExpiryMonth": "07",
    "cardExpiryYear": "2028",
    "cardBrand": "VISA",
    "cardIssuingCountry": "PL"
  },
  "amount": 11.12,
  "currency": "EUR",
  "customerAmount": 15,
  "customerCurrency": "USD",
  "redirectUrl": "http://init/txid/a0981ba1540d4062bc42d4019607sf94",
  "errorCode": "1.01",
  "externalResultCode": "03",
  "externalRefs": {
    "orderId": 123456
  },
  "customer": {
    "referenceId": "VIP_customer_12345",
    "citizenshipCountryCode": "GB",
    "firstName": "Harry",
    "lastName": "Potter",
    "dateOfBirth": "1996-01-05",
    "email": "customer@email.com",
    "phone": "357 123456789",
    "locale": "en",
    "ip": "172.16.0.1",
    "routingGroup": "VIP_Campaign",
    "kycStatus": true,
    "paymentInstrumentKycStatus": true,
    "dateOfFirstDeposit": "2021-02-23",
    "depositsAmount": 1000,
    "withdrawalsAmount": 250,
    "depositsCnt": 12,
    "withdrawalsCnt": 3,
    "trustLevel": "ftd",
    "btag": true,
    "affiliated": "yes"
  },
  "billingAddress": {
    "addressLine1": "211, Victory street",
    "addressLine2": "Office 7B",
    "city": "Hogwarts",
    "countryCode": "GB",
    "postalCode": "01001",
    "state": "CA"
  },
  "startRecurring": true,
  "recurringToken": "string",
  "terminalName": "string"
}"""
signature = "aca727a6c369af591969690b892d4ab0c2075176b25dcde50be911369b2d38ee"

encoded_body = b'{\r\n  "id": "12345",\r\n  "referenceId": "payment-123",\r\n  "paymentType": "DEPOSIT",\r\n  "state": "COMPLETED",\r\n  "description": "Funding the account",\r\n  "parentPaymentId": "a0981ba1540d4062bc42d4019607sf94",\r\n  "paymentMethod": "BASIC_CARD",\r\n  "paymentMethodDetails": {\r\n    "customerAccountNumber": "400000***0002",\r\n    "cardholderName": "Harry Potter",\r\n    "cardExpiryMonth": "07",\r\n    "cardExpiryYear": "2028",\r\n    "cardBrand": "VISA",\r\n    "cardIssuingCountry": "PL"\r\n  },\r\n  "amount": 11.12,\r\n  "currency": "EUR",\r\n  "customerAmount": 15,\r\n  "customerCurrency": "USD",\r\n  "redirectUrl": "http://init/txid/a0981ba1540d4062bc42d4019607sf94",\r\n  "errorCode": "1.01",\r\n  "externalResultCode": "03",\r\n  "externalRefs": {\r\n    "orderId": 123456\r\n  },\r\n  "customer": {\r\n    "referenceId": "VIP_customer_12345",\r\n    "citizenshipCountryCode": "GB",\r\n    "firstName": "Harry",\r\n    "lastName": "Potter",\r\n    "dateOfBirth": "1996-01-05",\r\n    "email": "customer@email.com",\r\n    "phone": "357 123456789",\r\n    "locale": "en",\r\n    "ip": "172.16.0.1",\r\n    "routingGroup": "VIP_Campaign",\r\n    "kycStatus": true,\r\n    "paymentInstrumentKycStatus": true,\r\n    "dateOfFirstDeposit": "2021-02-23",\r\n    "depositsAmount": 1000,\r\n    "withdrawalsAmount": 250,\r\n    "depositsCnt": 12,\r\n    "withdrawalsCnt": 3,\r\n    "trustLevel": "ftd",\r\n    "btag": true,\r\n    "affiliated": "yes"\r\n  },\r\n  "billingAddress": {\r\n    "addressLine1": "211, Victory street",\r\n    "addressLine2": "Office 7B",\r\n    "city": "Hogwarts",\r\n    "countryCode": "GB",\r\n    "postalCode": "01001",\r\n    "state": "CA"\r\n  },\r\n  "startRecurring": true,\r\n  "recurringToken": "string",\r\n  "terminalName": "string"\r\n}'

sign = hmac.new(
    key=settings.PAYADMIT_SIGN_KEY.encode(), msg=encoded_body, digestmod=hashlib.sha256
).hexdigest()

print(f"Signature: {sign}")
