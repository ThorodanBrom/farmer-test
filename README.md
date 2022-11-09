1. Make virtualenv and install requirements
```
virtualenv -p python3 .
pip3 install -r requirements.txt
```
2. Download `chromedriver` from [here](https://sites.google.com/chromium.org/driver/). You also need to have Chrome/Chromium installed. The version of `chromedriver` depends upon the the version of Chrome/Chromium you have installed, so install the right version.

3. Extract the `chromedriver` binary and place it in `/usr/local/bin`

4. Create a directory to store the downloaded files
```
mkdir /home/user/results
```
4. Run the script and include the full path of the directory created in previous step
```
python3 ch_get_stuff.py /home/user/results
```
