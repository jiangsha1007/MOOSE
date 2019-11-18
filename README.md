# MOOSE
Monitoring and evaluation system of open source ecosystem
# Research background
## Understanding the "state" of the open source software ecosystem
- Researchers can monitor the ecosystem and understand its current situation and development trend;  
- Developers can choose active and potential ecosystems for development;  
- Manager can timely adjust the project development process;  
- Users select "good quality" projects

## Up to now, the evaluation of open source software and ecosystem is mostly based on the subjective factors of the evaluators, mainly on the perceptual analysis, lacking of scientific objective quantitative methods

# Framework
## MOOSE_CORE
### The core module of moose system is mainly used for scheduling other modules, analysis and calculation. The main functions include:
- Get project source code  
- Analyze git log  
- Analyze source code defects  
- Statistics of crawling data  
- Manage the operation of crawlers and other modules  
> Analyze git log data, mainly obtain LOC, number of files, number of developers, project active time, commit statistics, developer active data, etc.  
> The statistical data include but are not limited to the following data:  
> - Issue close ratio  
> - Pull merge ratio  
> - Number of issue, pull request, comment and review of core developers
> - Issue close time
> - Pull request merge time

## MOOSE_SPIDER
### Regularly crawling the data of software projects in the monitored open source ecosystem. Use python-scraper framework. Crawling data includes but is not limited to the following data:

-  Basic data of the project (star, fork, subscribe, create time, owner, language, description, license and so on)
- Issue data  
- Pull request data  
- Commit data  
- Various comment data  
- Review data  
- Topic data  
- User data  
...

## MOOSE_WEB
### This module is the interactive interface between the user and the system, and uses the python Django framework
> Users can generate the ecosystem they need to monitor, just as it is convenient to generate a song list.  
> Provide exquisite and rich data report presentation.  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/1.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/2.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/3.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/4.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/5.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/6.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/7.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/8.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/9.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/10.png)  
![Image text](https://github.com/jiangsha1007/MOOSE/raw/master/MOOSE_web/image-folder/11.png) 

# Next work  
- Modularize each module to facilitate the addition of subsequent functions  
- Rich data types, including developer network map, emotion analysis, bug analysis, etc  
- Optimize data crawling and code download performance

# Contact
- Email:jiangsha1007@sjtu.edu.cn  
- Wechat:jiangxxs Remarks:MOOSE