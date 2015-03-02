#FFS  
Free & For Sale. Centralizing sales information.  

##Setup
###Requirements  
Install using "pip install <package_name>"
  
  
* flask  
* flask-sqlalchemy  
* flask-bootstrap  
* flask-wtf  
* apscheduler  
* python-dateutil  
* facebook-sdk  
* praw  

###How to start server  
```
python run.py
```  
Go to [http://localhost:5000/market/browse](http://localhost:5000/market/browse)  
  
#TODO or Roadmap 

##High priority
  
* Retain query on search  
  * fill out form based on URL
* User login
* Personalize groups/location  
* Keyword notifications  

##Medium priority
  
  
* include /r/buildapcsales and other post-based systems  
  * reformat comment system to allow for nesting (reddit support)  
* add REST-ful post preview /post/id  

##Lower priority
  
  
* Natural language processing to filter out non-sale posts  
* Price history & d3.js graphical analysis  
* view your own post history  
* manage posts & sync changes  
