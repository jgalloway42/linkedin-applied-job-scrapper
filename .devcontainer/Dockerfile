FROM python:3.11-slim

# Install Google Chrome (modern key method — apt-key removed in Debian 13)
# Also install Xvfb + noVNC so Chrome is viewable in Codespaces via port forwarding
RUN apt-get update && apt-get install -y wget gnupg ca-certificates \
       xvfb x11vnc novnc websockify \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub \
       | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set the virtual display so Chrome knows where to render
ENV DISPLAY=:99

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# reports/ is bind-mounted at runtime so output persists on the host
VOLUME /app/reports
