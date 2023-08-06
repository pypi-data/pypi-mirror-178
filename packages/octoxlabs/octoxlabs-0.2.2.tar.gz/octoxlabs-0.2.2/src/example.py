# Octoxlabs
from octoxlabs import OctoxLabs

octo = OctoxLabs(ip="localhost", token="aeaf4b4578455c66132b9e5e2d1e6bbc5d3b305b")

count, queries = octo.get_queries()
print(count)
print(queries)
# discovery = octo.get_last_discovery()

q = octo.get_query_by_name(query_name="cool")
print(q)
print(q.add_tag("ahmet"))
print(q.add_tag("ahmet2"))
print(octo.get_query_by_name(query_name="cool"))

q.name = "cool2"
q.save()
print(octo.get_query_by_name(query_name="cool2"))

#
# print(octo.get_device_detail(hostname="centos7mariadb", discovery=discovery))
#
# print(discovery.parsed_start_time)
# print(discovery.parsed_end_time)
# print(type(discovery.parsed_end_time))


