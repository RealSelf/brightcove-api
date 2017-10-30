A Python 2.7 wrapper for Brightcove's Analytics API.

# Example Usage

```
from brightcove_api import Brightcove
import os

client_id = os.environ['BRIGHTCOVE_CLIENT']
client_secret = os.environ['BRIGHTCOVE_SECRET']

brightcove = Brightcove(client_id, client_secret)

brightcove.get_video_data(accounts, dimensions, fields, video_id, from_date)
```

For more details please refer to the [Brightcove Analytics API documentation](https://support.brightcove.com/overview-analytics-api-v1)