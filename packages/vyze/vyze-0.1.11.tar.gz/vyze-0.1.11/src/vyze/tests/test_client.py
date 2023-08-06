from .test_system import service_url, system_url
from ..client import Client, Pipe
from ..system import SystemClient, read_layer_profile
from ..service import ServiceClient


profile_token = '...'
service_token = '...'

service_url_loc = service_url
system_url_loc = system_url


def test_client__load_universe():
    client = Client(ServiceClient(), SystemClient())
    client.service_client.set_token(service_token)
    client.system_client.set_layer_profile(read_layer_profile(profile_token))
    client.service_client.load_universe('vergleichsportal')

    print()

    # pipe = Pipe('$getItem')
    # items = client.get_objects(pipe)
    # for item in items:
    #     print(item)
    #
    # print()
    #
    # pipe = Pipe('$getItem').order('name')
    # items = client.get_objects(pipe)
    # for item in items:
    #     print(item)
    #
    # print()
    #
    # pipe = Pipe('$getItem').order('id')
    # items = client.get_objects(pipe)
    # for item in items:
    #     print(item)
    #
    # print()
    #
    # pipe = Pipe('$getItem').order('itemId')
    # items = client.get_objects(pipe)
    # for item in items:
    #     print(item)

    # items = get_item_pipe.model('item').filter('itemId', 'eq', '7743023').get_objects()
    # print(items)

    # print()
    #
    # pipe = Pipe('$getItem').filter('itemId', 'eq', '7743023')
    # items = client.get_objects(pipe)
    # for item in items:
    #     print(item)

    print()

    pipe = Pipe('$putCrawljob')
    crawljob = client.put_object(pipe, {'running': True})
    print(crawljob)

    # items = get_item_pipe.model('item').filter('itemId', 'eq', '7743023').get_objects()
    # print(items)


    # Pipe(client, 'on item [name = %name] -> %node').params(name="Test", node=Pipe())