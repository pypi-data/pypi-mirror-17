=====
Usage
=====

To use smokesignal in a project::

    import smokesignal

	# Create a client to communicate with etcd
	# You can use either: host, port or use dins discovery, this requires the appropriate srv records to be set
	ss_client = smokesignal.Client(host = 'example.com', port = 2379)
	# Or ss_client = smokesignal.Client(dns = 'example.com')

	# A service is described as an instance of smokesignal.Service
	# The default mode is http
	# They can be routed via a subdomain or uri or a combination of the two
	web_server = smokesignal.Sevice(name = 'web', subdomain = 'blog') # Will be reachable at the blog.exmple.com
	api_server = smokesignal.Service(name = 'api', subdomain = 'blog', uri = 'api') # At blog.example/api
	static_server = smokesignal.Service(name = 'static_assets', uri = 'static') # At example.com/static
	# tcp mode requires a service_port, the port that the frontend will on listen for connections.
	tcp_server = smokesignal.Service(name = 'tcpService', mode = 'tcp', service_port = 4000)

	# Any number of backends can be added to a service
	web_backend = smokesignal.Backend(host = 'web.backends.example.com', port = 80)
	api_backend1 = smokesignal.Backend(host = 'api1.backends.example.com', port = 3456)
	api_backend2 = smokesignal.Backend(host = 'api2.backends.example.com', port = 3456)
	static_backend = smokesignal.Backend(host = 'static.backends.example.com', port = 80)

	web_server.addBackend(web_backend)
	api.server.addBackend(api_backend1)
	api.server.addBackend(api_backend2)
	static_server.addBackend(static_backend)

	# Finally register the service with the client
	ss_client.register(service = web_server)
	ss_client.register(service = api_server)
	ss_cliet.register(static_server)

	# To simplify adding services and backends all keywords can be passed to register
	ss_client2 = smokesignal.Client(dns = 'example1.com')
	ss_client2.register(name = 'web', subdomain = 'blog', host = 'web.backends.example.com', port = 80) # The same as web_server
	ss_client2.register(name = 'api', subdomain = 'blog', uri = 'api', host = 'api1.backends.example.com', port = 3456) # As api_server
	# To add multiple backends simple call register again omitting everything, but the name, host and port
	ss_client2.register(name = 'api', host = 'api2.backends.example.com', port = 3456)
