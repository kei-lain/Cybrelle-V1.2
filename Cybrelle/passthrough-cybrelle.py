address = Host.objects.filter(ip_addres=ip_address)
username = Host.objects.filter(username=username)
password = Host.objects.filter(password=password)
schema = HostSchema.from_django(Host)
with concurrent.futures.ProcessPoolExecutor() as executor:
    for address, username, password in itertools.izip(addresses,usernames,passwords):
        result = executor.submit(Scanner,address, username, password)
        return{result}