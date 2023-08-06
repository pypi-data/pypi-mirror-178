**csvtickerlist**

A simple package that allows users the ability to generate a CSV file that contains a full list of all active ticker symbols on the marketplace. This package uses a headless, Selenium Chrome browser to fetch this CSV file.


The CSV file contains ticker symbols, along with some basic information (i.e. Share price, count, industry, etc.) NASDAQ hosts this information in its entirety for free and this module only requires making one page request to retrieve the CSV file.


## Example


```python
from csvtickerlist import GetCSV

def GetDataFolder():
	return filedialog.askdirectory(title = 'Select Folder')

def main():
	folder = GetDataFolder()
	GetCSV.GetCSVFile(folder, 10)

	#arg1 (folder) represents the output folder
	#arg2 (10) represents the seconds to wait before closing the web driver.
	#10 seconds is recommended, but increase this when facing connectivity issues.

```



To-Do:

- Add functionality for a filtered output (i.e. valuation range, industry selections, etc.)
