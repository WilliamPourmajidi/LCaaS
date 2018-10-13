# LCaaS

LCaaS is a Python-based blockchain tool. It receives data through its API and then use its internal blockchain framework to convert data to blocks and then pushes them to blockchain by establishing hash-binding relationship among blogs. 

Furthermore, LCaaS, introduces a solution for the common capacity challenges of the blockchains. In LCaaS, we have introduced a novel solution referred to as “Hierarchical ledger” or also known as “Multi-dimensional blockchains”.  For more information, navigate to google scholar page and search for “Logchain as a service” and have your fingers crossed, if you see something along the following lines, you are good to go! 

![screenshot](https://user-images.githubusercontent.com/18631688/46560397-9fcc2680-c8c1-11e8-9052-1beeb996d281.png)

LCaaS includes:

   - API for incoming traffic
   - Proprietary private blockchain implementation 
   - Integration with Firebase Realtime Database
   - Integration with Ethereum Test Network (Ropsten)
   - Configurable functionalities (check config.json for more information) 

### Tech

LCaaS uses a number of projects:

* [Firebase] - Google Real-time Database
* [Ropsten Test Network ] - Ethereum Test Network (based on PoW)

### Language and Libraries
LCaaS is designed and developed with Python 3.6 and make use of the following Python Libraries:

* pyrebase
* ethereum
* flask 
* hashlib
* TimeKepper
* json
* web3
* contract_abi

### Installation

Dillinger requires [Node.js](https://nodejs.org/) v4+ to run.

Download the source code and make sure you have the above libraries in your python environment, then, proceed with the following command: 

```sh
Python index.py
```

Since LCaaS runs its own internal web server, you should be able to open any broswer and put:


```sh
http://127.0.0.1:5000/
```
You should see the following message on your web-broswer indicating that LCaaS is running. 

![running](https://user-images.githubusercontent.com/18631688/46561106-2d107a80-c8c4-11e8-8b2d-3125429a6d2a.png)


### API Signature Examples:

*submit_raw (to submit the actual logs to LCaaS)
 ```sh
curl -X POST \
  http://127.0.0.1:5000/submit_raw \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: bd3bf06b-5d56-b35f-972f-31f104aea47b' \
  -d '{"Log": "User William formatted C Drive at 7:52 AM , Aug 16th, 2018"}' 
 ```
 ![submit_raw_optimized](https://user-images.githubusercontent.com/18631688/46905815-fc819f80-cec6-11e8-9e11-f2fe3aff2f33.gif)

 
 
 submit_digest (to submit the digest of logs to LCaaS)
 ```sh
curl -X POST \
  http://127.0.0.1:5000/submit_digest \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 60dc220e-d201-91e5-c331-6d456cb2a57e' \
  -d '{"digest": "10E721E49C013F00C62CF59F2163542A9D8DF02464EFEB615D31051B0FDDC327" }'
 ```
verify_raw to verify that if an actual raw log file is submitted to the LCaaS before or not. 
 
  ```sh
 curl -X POST \
  http://127.0.0.1:5000/verify_raw \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 23b7ce69-cbc3-e8dc-2e5c-bf4e1b44d9d4' \
  -d '{"Log": "User William formatted C Drive at 7:52 AM , Aug 16th, 2018"}'
  ```
  
  verify_digest to verify that if the digest of a log file is submitted to the LCaaS before or not. 
 
  ```sh
curl -X POST \
  http://127.0.0.1:5000/verify_digest \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: aa9bb524-11e4-74ea-d61c-e0c7f7c2fb10' \
  -d '{"digest": "10E721E49C013F00C62CF59F2163542A9D8DF02464EFEB615D31051B0FDDC327" }'
  ```
  verify_tb to verify the terminal block and ensure that the entire blocks in a circled blockchain are not tampered. 
  Did not understand a word? read the paper!  
 
 ```sh 
curl -X POST \
  http://127.0.0.1:5000/verify_tb \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: adfacf8b-1292-8644-574a-f6b959418727' \
  -d '{"tb_hash": "4aadc7120cf783fa3ce0b961edc12229aa2900c0d0d7238369181877e7892178" }'  
 ```
 
 
[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [Ropsten Test Network]: <https://ropsten.etherscan.io/>
   [firebase]: <https://firebase.google.com/>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
   
   
   
Comments and suggestions or questions? please send them to me at William.pourmajidi@gmail.com


