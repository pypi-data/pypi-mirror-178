import json
import logging
import sys
import traceback

from c8yrc.rest_client import CumulocityClient
from c8yrc.rest_client.c8y_exception import C8yException

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # my_device_address = '2102351HNDDMK2000759'.lower()
    _tenant = 't2700'
    # device = f'cb1-{my_device_address}'.strip()
    _host = 'main.dm-zz-q.ioee10-cloud.com'
    rest_user_name = 'service_schindler-jenkins'
    rest_user_password = '2txFLPmgE5xwWRovG7nW7e4Y94XhwOB3'

    client = CumulocityClient(hostname=_host, tenant=_tenant, user=rest_user_name, password=rest_user_password)
    session = client.retrieve_token()
    # client.get_firmware_info(device, 'c8y_Serial')
    my_data = dict(name="cb3-c8y-emmc-buster-armhf-prod-schindler", version="4.1.0_2022-11-14-1632",
                   type="os", device="cb3", devicetype="sch-cb3-dq-armhf")
    with open("bar.json", "w") as outfile:
        json.dump(my_data, outfile)
    try:
        client.upload_firmware(artifact_file_location='../tests/foo.mender', metadata_file_location='bar.json')
    except C8yException as e:
        traceback.print_exc()
        sys.exit(-1)

