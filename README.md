# Ning Gao

My Personal Portfolio on the web - [link to website](http://ninggaoboulder.com)  

# Technology

Developed using Python Flask, and Jinja.  

# Pre-requisite
sudo pip install flask  
sudo pip install flask-httpauth  
sudo pip install flask_sqlalchemy  
sudo pip install flask-wtf  
sudo pip install flask-mail  
## optional for uwsgi    
sudo pip install uwsgi  

# Run the service
If running using uwsgi
```
$ uwsgi --ini wsgi.ini &> wsgi.log &
```
nginx related configurations are in "*/etc/nginx/sites-available/default*"
<!---
#               location / {
#                   include uwsgi_params;
#                   uwsgi_pass unix:/$PROJECT_PATH/NingWebsite/ningwebsite.sock;
#               }
-->
