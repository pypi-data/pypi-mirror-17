# apicrafter
apicrafter helps people create simple HTTP APIs easily.

To start creating an API, all you need is a path, a function, and a method

For example:

```python
import apicrafter

def root_request_handler(request):
    request.respond("<b>Hello, world!</b>")

#Starts ApiServer on all interfaces on port 8080
my_server = apicrafter.ApiServer('all', 8080)

my_server.add_handler('/', root_request_handler, 'GET')

my_server.start()

```
Then, just navigate to http://localhost:8080 on the web browser of your choice!
