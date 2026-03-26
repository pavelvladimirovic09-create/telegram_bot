#!/bin/bash

echo "===== DEPLOY TELEGRAM BOT ====="

cd ~/telegram_bot || exit

echo "Обновляем ветку..."
git checkout master
git pull origin master

echo "Добавляем изменения..."
git add .

echo "Создаем коммит..."
git commit -m "auto deploy" 2>/dev/null

echo "Отправляем на GitHub..."
git push origin master

echo "Перезапускаем Railway..."
railway up --detach

echo ""
echo "Последние изменения в Git:"
git log -5 --oneline

echo ""
echo "DEPLOY ГОТОВ"
