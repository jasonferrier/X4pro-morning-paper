# Xteink X4 Pro guide

The paper is a plain EPUB (`read-later.epub`) kept as one book in your Calibre library. Get it onto the reader with **Calibre wireless** (needs CrossPoint firmware) or a manual upload (stock firmware).

Set `"device": "xteink"` in `config.json` (the default). After each build the EPUB is replaced in Calibre; if `export_dir` is set, a copy is also written there.

## Stock Licorice firmware

I could not verify that stock firmware has a Calibre wireless connection. Treat it as unsupported and use one of these:

1. **USB**: plug in USB-C, copy `read-later.epub` (from `export_dir` or Calibre's library folder) to the SD card root, or send it from Calibre ("Connect/share" > "Send to device") if Calibre detects it as a drive.
2. **Stock Wi-Fi book transfer**: if the firmware offers a browser upload page, open it and upload the EPUB.

Or install CrossPoint (below) to get the automatic path.

## Install CrossPoint firmware

CrossPoint is open source (https://github.com/crosspoint-reader/crosspoint-reader). Flashing carries risk: back up the SD card and keep the reader charged.

1. Use Chrome or Edge on a computer. Connect the X4 Pro by USB-C and wake it.
2. Open https://crosspointreader.com/#flash-tools, choose **Xteink X4Pro**, pick an official release, and flash.
3. If the device does not appear in the serial picker, try another cable, port or browser. If it is still missing, it may be USB-locked (common with third-party stores such as AliExpress; units bought from xteink.com are not). Use the Xteink Unlocker at https://crosspointreader.com/#unlock-tool and read its warnings. Only CrossPoint and CrossInk are supported there; flashing anything else can brick a locked unit.
4. Command line alternative (X4 Pro is ESP32-S3):
   ```
   pip install esptool
   esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 write_flash 0x10000 firmware.bin
   ```
   Get `firmware.bin` for the X4 Pro from the project's Releases page.
5. Revert: flash the official firmware again with the same web flasher.

## Install the Calibre plugin

1. Download the latest zip from https://github.com/crosspoint-reader/calibre-plugins/releases (for example `crosspoint_reader-v0.2.8.zip`). Do not unzip it.
2. Calibre > Preferences > Advanced > Plugins > **Load plugin from file**, pick the zip, accept the prompt, restart Calibre.
3. Optional: add the plugin's toolbar button via Preferences > Interface > Toolbars.

## Sync wirelessly

1. Reader and computer on the same Wi-Fi.
2. On the reader: File Transfer / **Calibre Wireless** mode (Connectivity menu). It joins your Wi-Fi and shows instructions.
3. In Calibre, use the CrossPoint device/connection (see plugin settings; enter the reader's IP if it is not discovered). Select the "Read Later" book and send it to the device.
4. The reader's upload will fail with "File already exists" if a file of the same name is on the SD card. Delete the old edition on the reader (or in its web file manager) first, or let the plugin overwrite if it offers that. The server accepts `POST /upload?overwrite=1`, so a script can replace it directly:
   ```
   curl -F "file=@read-later.epub" "http://crosspoint.local/upload?overwrite=1"
   ```
   with the reader in Calibre Wireless/File Transfer mode. Check `docs/webserver-endpoints.md` in the CrossPoint repo, since the API may change between releases.

Alternative without the plugin: in CrossPoint, add Calibre-Web or Calibre's content server as an OPDS server (Settings > OPDS; append `/opds` for Calibre) and download the paper from the on-device browser.

## Scheduling tips

Calibre wireless needs the reader awake, so the morning cron job only builds the EPUB; start Calibre wireless when you wake the reader. For hands-off delivery, set `export_dir` and push with the `curl` command above.

## Notes

- Reading-activity data comes from Kobo sync only; on Xteink that source is skipped and the interest model uses the others.
- Large images make the EPUB big on the reader's limited RAM; the cover is a single JPEG.
