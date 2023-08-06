This Modles requestsRenderJs will help you to scrap data from Java Script Render dynamic websites.

CODE EXAMPLE:

```
from requestsRenderJs.TechsunRequests import Requests

requests = Requests(save_response=True, show=True)

response = requests.Get('https://www.youtube.com/') # resp---> Html_response (str)
```


PARAMETERS:
save_response (optional)  -->   Save HTML page response in a raw.html file for analysis.
show                      -->   See browser opening if needs to render JS 
