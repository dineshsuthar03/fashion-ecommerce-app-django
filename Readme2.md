Complete Documentation: Deploying Django eCommerce Project in Production
1. Prerequisites
Before proceeding, ensure the following are in place:

You have a Django eCommerce project set up.
You have an Ubuntu server (or any Linux server).
You have SSH access to the server and the required permissions.
Python 3.x, pip, virtualenv, and Git are installed.
Your server has a domain name.
You have configured the security group on your cloud provider to allow inbound traffic on port 80 (HTTP) and port 443 (HTTPS).
2. Set Up the Server Environment
Step 1: SSH into your server
bash
Copy code
ssh username@your-server-ip
Step 2: Update the system
Ensure your server is up to date with the latest packages:

bash
Copy code
sudo apt update && sudo apt upgrade -y
Step 3: Install Required Packages
Install the necessary packages:

bash
Copy code
sudo apt install -y python3-pip python3-dev libpq-dev nginx git curl
Step 4: Install and Set Up Virtual Environment
Install virtualenv if it's not already installed:

bash
Copy code
sudo apt install -y python3-venv
Navigate to your project directory and create a virtual environment:

bash
Copy code
cd /home/username/your-project-directory
git clone https://github.com/your-repository/project-name.git
cd project-name
python3 -m venv venv
Activate the virtual environment:

bash
Copy code
source venv/bin/activate
Install the required Python dependencies:

bash
Copy code
pip install -r requirements.txt
3. Set Up Gunicorn
Step 1: Install Gunicorn
Install Gunicorn in your virtual environment:

bash
Copy code
pip install gunicorn
Step 2: Test Gunicorn
Test that Gunicorn is working by running:

bash
Copy code
gunicorn --workers 3 --bind 0.0.0.0:5004 projectname.wsgi:application
This binds Gunicorn to 0.0.0.0:5004. You should be able to access the app via http://your-server-ip:5004.

4. Set Up Nginx as a Reverse Proxy
Step 1: Configure Nginx
Create an Nginx server block configuration for your app:

bash
Copy code
sudo nano /etc/nginx/sites-available/projectname
Add the following configuration, replacing the placeholders with your paths and domain:

nginx
Copy code
server {
    listen 80;
    server_name your-domain.com;  # Your domain name

    location / {
        proxy_pass http://127.0.0.1:5004;  # Gunicorn is listening on this port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/username/your-project-directory/staticfiles/;  # Static files location
    }

    location /media/ {
        alias /home/username/your-project-directory/public/media/;  # Media files location
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /usr/share/nginx/html;
    }
}
Step 2: Enable the Nginx Site Configuration
Create a symbolic link in the sites-enabled directory:

bash
Copy code
sudo ln -s /etc/nginx/sites-available/projectname /etc/nginx/sites-enabled
Test the Nginx configuration to ensure there are no errors:

bash
Copy code
sudo nginx -t
Restart Nginx:

bash
Copy code
sudo systemctl restart nginx
Ensure Nginx starts on boot:

bash
Copy code
sudo systemctl enable nginx
5. Set Up Gunicorn as a Systemd Service
To manage the Gunicorn process automatically and ensure it restarts on failure, we'll set it up as a systemd service.

Step 1: Create the Gunicorn service file
Create a new service file for Gunicorn:

bash
Copy code
sudo nano /etc/systemd/system/projectname.service
Add the following configuration:

ini
Copy code
[Unit]
Description=Gunicorn server for projectname
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/username/your-project-directory
ExecStart=/home/username/your-project-directory/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5004 projectname.wsgi:application

[Install]
WantedBy=multi-user.target
Step 2: Start and Enable Gunicorn Service
Reload systemd to register the new service:

bash
Copy code
sudo systemctl daemon-reload
Start the Gunicorn service:

bash
Copy code
sudo systemctl start projectname
Enable the service to start on boot:

bash
Copy code
sudo systemctl enable projectname
Check the status of the Gunicorn service:

bash
Copy code
sudo systemctl status projectname
6. Set Up Static and Media Files
Step 1: Collect Static Files
Run the following command to collect static files into the STATIC_ROOT:

bash
Copy code
python manage.py collectstatic
Step 2: Configure File Permissions
Ensure that the Nginx user has access to static and media files:

bash
Copy code
sudo chown -R www-data:www-data /home/username/your-project-directory/staticfiles
sudo chown -R www-data:www-data /home/username/your-project-directory/public/media
7. Final Testing
Test your application by navigating to http://your-domain.com in your browser.

Ensure that both the Gunicorn server and Nginx are working correctly.

Check the logs for errors if you encounter issues:

Gunicorn logs:

bash
Copy code
sudo journalctl -u projectname.service
Nginx logs:

bash
Copy code
sudo tail -f /var/log/nginx/error.log
8. Enable HTTPS (Optional but Recommended)
To secure your site with HTTPS, you can use Let's Encrypt and Certbot:

Step 1: Install Certbot and Nginx Plugin
bash
Copy code
sudo apt install certbot python3-certbot-nginx
Step 2: Obtain SSL Certificate
Run Certbot to automatically configure SSL for Nginx:

bash
Copy code
sudo certbot --nginx -d your-domain.com
Step 3: Test SSL Renewal
Ensure the SSL certificate renews automatically:

bash
Copy code
sudo certbot renew --dry-run
Conclusion
Your Django eCommerce project is now deployed on a production server using Gunicorn and Nginx, and it's being managed as a service using systemd.

This setup provides a scalable and production-ready environment, and using Nginx as a reverse proxy allows handling static files efficiently while Gunicorn serves the dynamic content.