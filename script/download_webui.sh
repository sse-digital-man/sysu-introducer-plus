#!/bin/sh

url="https://github.com/sse-digital-man/sysu-introducer-controller/releases/download/v0.0.0/dist.zip"

if [ -d "dist.zip" ]; then
    rm "dist.zip"
fi

curl -LJO $url

if [ -d "static" ]; then
    rm -r static
fi

unzip -q dist
mv dist static
rm dist.zip