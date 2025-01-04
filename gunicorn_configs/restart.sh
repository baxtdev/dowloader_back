sudo systemctl daemon-reload
sudo systemctl restart downloader_back.socket downloader_back.service telegram_bot_1.service
sudo sudo nginx -t && sudo systemctl restart nginx