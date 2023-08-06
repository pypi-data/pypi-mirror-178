get-course

This is the package used to get the exchange rate. It works with https://currate.ru/

Function:

1) Getting courses from different countries

Attribut:

    get_course(render=str, valut=bool, key_list=bool)

    render=str - from which to which currency to transfer
    valut=bool(optional) - print result with currency
    key_list=bool(optional) - get a list of currencies

Install:

    pip install get-course==last_version

EXAMPLE:

    from get_course import get_course

    print(get_course('usdrub', valut=True))