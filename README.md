# Open Redirect Toolkit
![alt text](https://github.com/corneacristian/Open-Redirect-Toolkit/blob/master/logo_OPT.png)

This toolkit helps bug bounty hunters, researchers, students and cyber security experts to automatically find and validate Open Redirect vulnerabilities. (for more details about what is an Open Redirect and what is its impact: https://cwe.mitre.org/data/definitions/601.html)



## Requirements
pip install bs4 requests python-dotenv

## Search for a vulnerable target
python find_redirect.py [domain]   

example: python find_redirect.py mysecuredomain101.com

The tool will search for potential Open Redirects on the domain provided, but also on its subdomains too, which is really useful if you are doing Bug Bounty.


## Exploit the target
python exploit_redirect.py [full URL]

example: python exploit_redirect.py https://mysecuredomain101.com/index.php?link=

The tool will try to exploit the target using various payloads that can also bypass Open Redirect protection mechanisms.

## Thanks 

@ak1t4
@meibenjin
