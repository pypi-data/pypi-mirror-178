# DataTower.ai

This is the official Python SDK for DataTower.ai.

## Easy Installation

You can get DataTower.ai SDK using pip.

pip install dtsdk

Once the SDK is successfully installed, use the SDK likes:

python

from dtsdk.sdk import DTAnalytics,DebugConsumer

dt = DTAnalytics(DebugConsumer(app_id="app_id_xxxx", token="xxxxxxxxxxxxxxxxxxxxxxx",server_url="https://xxxx"))

properties={"abc":123,"bcd":"xxx"}

dt.track(dt_id="aaaa",acid='bbbb',event_name="ad_click",properties=properties)

dt.flush()

dt.close()


