# Python Vizio Controller

## Based on https://github.com/vkorn/pyvizio

```
python3 -m pip install viziocontroller
```

### 1.) Run and Generate Request Token

```
import viziocontroller
if __name__ == "__main__":
	tv = viziocontroller.VizioController({
			"name": "Loft TV" ,
			"mac_address": "2c:64:1f:25:6b:3c" ,
			"ip": "192.168.1.100" ,
		})
```

### 2.) Run again and Generate Access Token

```
import viziocontroller
if __name__ == "__main__":
	tv = viziocontroller.VizioController({
			"name": "Loft TV" ,
			"mac_address": "2c:64:1f:25:6b:3c" ,
			"ip": "192.168.1.100" ,
			"request_token": 512003,
			"code_displayed_on_tv": 6108 ,
		})
```

### Run from Now On

```
import viziocontroller
if __name__ == "__main__":
	tv = viziocontroller.VizioController({
			"name": "Loft TV" ,
			"mac_address": "2c:64:1f:25:6b:3c" ,
			"ip": "192.168.1.100" ,
			"access_token": "Zhehzvszfq"
		})
```