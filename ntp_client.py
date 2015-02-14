import time
import os

ntp_server = 'master.team4.uclaclass.isi.deterlab.net'

try:
    import ntplib
    client = ntplib.NTPClient()
    response = client.request(ntp_server)
    offset = response.offset
    print offset
    # offset = time in ntp_server - time in ntp_client

except:
    print('Could not sync with time server.')
