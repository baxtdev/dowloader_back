ln -s /var/www/downloader_back/gunicorn_configs/telegram_bot_1.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start telegram_bot_1
sudo systemctl enable telegram_bot_1
