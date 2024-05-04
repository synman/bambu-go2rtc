#!/usr/bin/env python3

import struct
import os
import socket
import ssl
import time

username = 'bblp'
access_code = os.environ['PRINTER_ACCESS_CODE']
hostname = os.environ['PRINTER_ADDRESS']
port = 6000

MAX_CONNECT_ATTEMPTS = 12

auth_data = bytearray()
connect_attempts = 0

auth_data += struct.pack("<I", 0x40)   # '@'\0\0\0
auth_data += struct.pack("<I", 0x3000) # \0'0'\0\0
auth_data += struct.pack("<I", 0)      # \0\0\0\0
auth_data += struct.pack("<I", 0)      # \0\0\0\0
for i in range(0, len(username)):
    auth_data += struct.pack("<c", username[i].encode('ascii'))
for i in range(0, 32 - len(username)):
    auth_data += struct.pack("<x")
for i in range(0, len(access_code)):
    auth_data += struct.pack("<c", access_code[i].encode('ascii'))
for i in range(0, 32 - len(access_code)):
    auth_data += struct.pack("<x")

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

jpeg_start = bytearray([0xff, 0xd8, 0xff, 0xe0])
jpeg_end = bytearray([0xff, 0xd9])

read_chunk_size = 4096 # 4096 is the max we'll get even if we increase this.

# Payload format for each image is:
# 16 byte header:
#   Bytes 0:3   = little endian payload size for the jpeg image (does not include this header).
#   Bytes 4:7   = 0x00000000
#   Bytes 8:11  = 0x00000001
#   Bytes 12:15 = 0x00000000
# These first 16 bytes are always delivered by themselves.
#
# Bytes 16:19                       = jpeg_start magic bytes
# Bytes 20:payload_size-2           = jpeg image bytes
# Bytes payload_size-2:payload_size = jpeg_end magic bytes
#
# Further attempts to receive data will get SSLWantReadError until a new image is ready (1-2 seconds later)
while connect_attempts < MAX_CONNECT_ATTEMPTS:
    try:
        with socket.create_connection((hostname, port)) as sock:
            try:
                connect_attempts += 1
                sslSock = ctx.wrap_socket(sock, server_hostname=hostname)
                sslSock.write(auth_data)
                img = None
                payload_size = 0

                status = sslSock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                # LOGGER.debug(f"{self._client._device.info.device_type}: SOCKET STATUS: {status}")
                if status != 0:
                    # LOGGER.error(f"{self._client._device.info.device_type}: Socket error: {status}")
                    pass
            except socket.error as e:
                # LOGGER.error(f"{self._client._device.info.device_type}: Socket error: {e}")
                pass

            sslSock.setblocking(False)
            while True:
                try:
                    dr = sslSock.recv(read_chunk_size)
                    #LOGGER.debug(f"{self._client._device.info.device_type}: Received {len(dr)} bytes.")

                except ssl.SSLWantReadError:
                    #LOGGER.debug(f"{self._client._device.info.device_type}: SSLWantReadError")
                    time.sleep(1)
                    continue

                except Exception as e:
                    # LOGGER.error(f"{self._client._device.info.device_type}: A Chamber Image thread inner exception occurred:")
                    # LOGGER.error(f"{self._client._device.info.device_type}: Exception. Type: {type(e)} Args: {e}")
                    time.sleep(1)
                    continue

                if img is not None and len(dr) > 0:
                    img += dr
                    if len(img) > payload_size:
                        # We got more data than we expected.
                        # LOGGER.error(f"Unexpected image payload received: {len(img)} > {payload_size}")
                        # Reset buffer
                        img = None
                    elif len(img) == payload_size:
                        # We should have the full image now.
                        if img[:4] != jpeg_start:
                            pass
                            # LOGGER.error("JPEG start magic bytes missing.")
                        elif img[-2:] != jpeg_end:
                            pass
                            # LOGGER.error("JPEG end magic bytes missing.")
                        else:
                            # Content is as expected. Send it.
                            #os.write(1, img)
                            #os.write(1, b"--boundary\n")
                            #os.write(1, b"Content-Type: image/jpeg\n")
                            #os.write(1, b"Content-Length: %d\n\n" % len(img))
                            os.write(1, img)
                            #os.write(1, b"\n");

                        # Reset buffer
                        img = None
                    # else:     
                    # Otherwise we need to continue looping without reseting the buffer to receive the remaining data
                    # and without delaying.

                elif len(dr) == 16:
                    # We got the header bytes. Get the expected payload size from it and create the image buffer bytearray.
                    # Reset connect_attempts now we know the connect was successful.
                    connect_attempts = 0
                    img = bytearray()
                    payload_size = int.from_bytes(dr[0:3], byteorder='little')

                elif len(dr) == 0:
                    # This occurs if the wrong access code was provided.
                    # LOGGER.error(f"{self._client._device.info.device_type}: Chamber image connection rejected by the printer. Check provided access code and IP address.")
                    # Sleep for a short while and then re-attempt the connection.
                    time.sleep(5)
                    break

                else:
                    # LOGGER.error(f"{self._client._device.info.device_type}: UNEXPECTED DATA RECEIVED: {len(dr)}")
                    time.sleep(1)

    except Exception as e:
        pass
        # LOGGER.error(f"{self._client._device.info.device_type}: A Chamber Image thread outer exception occurred:")
        # LOGGER.error(f"{self._client._device.info.device_type}: Exception. Type: {type(e)} Args: {e}")
        # if not self._stop_event.is_set():
        #     time.sleep(1)  # Avoid a tight loop if this is a persistent error.
