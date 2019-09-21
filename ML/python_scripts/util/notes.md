# Notes
## TODO
- modify the scraping script to save progress of the download
    - save the plant you're on, and the # photo youre on as well
    - write this to a file, use os.path.isfile() to see if there is one and if so, load it and encorporate it

## Most common house plants

### To be added to JSON
- croton
- lemon lime dracaena
- moth orchid
- anthurium
- golden pothos
- lucky bamboo
- dracaena marginata
- snake plant
- peace lily
- ponytail palm
- majesty palm

## Confusion matrix findings
- remove common houseleek (done)
- remove ragworts (done)
- remove lace aloe (done)
- remove burros tail (done)
- 

## Design notes

### Single use method
if there is a save file present with valid save info, call this function for the first plant and then call the other (general) method for the remaining entries
- remove special checks from general method

### Save file
first check if the save file exists (aka not fresh batch)
- os.path.isfile(path)
if so read save file BEFORE calling the scrape method to pick up on the index
- might have to add new param to scrape method to take an index of the plant array 
	- is there overloading in python (?)

structure for the save file:

json file with:
- name of the plant being downloaded
- last succesful download
	- name and number 
- marker for pickup 
	- either:
		- index of following image (make sure not to mess up the file names)
			- make this in the script (lastdDownloadedIndex + 1)
		- or, index in the array of all plants (from other json file)
			- instead of marking the next plant in queue, just mark this one
			- if last plant in queue, set to null (not empty!)

example json file:
{
	"lastDownload":
	{
		"complete": false,
		"name": "aloe",
		"scientificName": "aloe vera",
		"lastDownloadedIndex": 200,
		"plantIndex": 4 
	}
}

- remove name and scientific name section (we dont need it actually)

- add a timeout feature to kill an image taking too long to load



## Bugs
#### Immediate
- ~~the save feature will save on the first instance of the loop even if it loaded a pickup index~~
- ~~after finishing a plant, it will read last plant's pickup data, making it so that the next plant will pull less images/be less efficient~~
	-~~ only read the save file ***only*** once when the script starts up~~
#### Non-immediate
-~~ should close the browser after every plant pull is done, not when _all_ the pulls are done~~

## Current Focus
### USDA Dataset
#### TODO:
1. ~~read the csv data~~
	- ~~only columns we care about are the scientific name and the common name (if there is one)~~
2. ~~process and reformat the data to fin into the json format~~
	- TODO: remove the "quality" tag in the json
3. check (manually or otherwise) for duplicates between the existing json and the new data 
	- maybe a non-problem? investigate firther
4. re-fetch images with new data
5. train model on-device (using createML)
6. test
	- ask for houseplant images maybe?























































