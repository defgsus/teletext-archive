# archive of german online teletexts

Or *videotext*, as we used to call it. 

This repo exists mainly because it's just possible to scrape those
online teletexts with github actions. And, you know, interesting
stuff might evolve from historic beholding.

The data is collected raw in [docs/snapshots](docs/snapshots). Each commit
adds, overwrites or removes the individual files of each teletext page.

Oh boy, look what else exists in the web: https://archive.teletextarchaeologist.org


## TODO

- **WDR** https://www1.wdr.de/wdrtext/index.html

  It's embedded in the main page and the urls seem somewhat complicated:
  
  https://www1.wdr.de/wdrtext/externvtx100~_eam-28f2b7a86d7cfcc43a2229d39ddabddd_eap__page__num-101.html?eap=8oI34N4hym4RDV6dhKK0OoKFhY2OtqKgnFTMkq%2B3SyVkbMnioITO25epQsdxUBuV7uhF9MzhhmSfKXfTmMgdIT1DK0SKlKChN%2BgMGumoVSFzMJ%2BUFF2YOcqyBktK2TLI
  
- **SR** https://www.saartext.de/100

  Embedded in a bigger page and subpage info needs to be scraped from html 
  
- **SWR** https://www.swrfernsehen.de/videotext/index.html

  They only deliver gif files, boy!

- **ARD** https://www.ard-text.de/

  Embedded in bigger page
  
- **3sat** https://blog.3sat.de/ttx/

  They have a nice collection of gif fonts. Problem is, they construct a 
  teletext image from those font-maps via html/css. oO
  
- **KIKA** https://www.kika.de/kikatext/kikatext-start100.html

  Images once more

### beyond the borders

- **CT** https://www.ceskatelevize.cz/teletext/ct/

  Images

- **Swiss Teletext** https://mobile.txt.ch/  
  
  Does not really seem to work - with my script-blockers anyways

- **ORF** https://teletext.orf.at/

  JSON API delivering ... image-urls
  