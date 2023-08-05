from pprint import pprint

import native_sdk_core

# https://app.swaggerhub.com/apis/IVANFOK/fast-api/0.1.0


def main():
    venue = "zerox"
    chain = "ethereum"
    pair = "ETH_USDT"
    side = "buy"
    indicative_quote_amount = 0.084
    firm_quote_amount = 112.198
    address = "0x0bab5b91cd87ad71dcbbd3885aa52bb3cffe26c9"
    token = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

    configuration = native_sdk_core.Configuration()
    configuration.api_key["api_key"] = "askdjflwihe"

    api_instance = native_sdk_core.DefaultApi(
        native_sdk_core.ApiClient(configuration=configuration)
    )

    response = api_instance.get_instruments(chain=chain)
    print("get_instruments: ", response)

    response = api_instance.get_indicative_quote(
        pair=pair,
        chain=chain,
        side=side,
        amount=indicative_quote_amount,
        address=address,
    )
    print("get_indicative_quote: ", response)

    response = api_instance.get_firm_quote(
        pair=pair,
        chain=chain,
        side=side,
        amount=firm_quote_amount,
        address=address,
    )
    print("get_firm_quote: ", response)

    response = api_instance.get_allowance(token=token, address=address, chain=chain)
    print("get_allowance: ", response)

    response = api_instance.get_balance(token=token, address=address, chain=chain)
    print("get_balance: ", response)


if __name__ == "__main__":
    main()
