# =========================================================================
# Dockerfile — ChurnGuard static site
# Serves the pre-built static files via a lightweight Nginx image.
# No build stage needed since this is a plain HTML/CSS/JS project.
# =========================================================================

FROM nginx:1.27-alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy project files into nginx's web root
COPY index.html /usr/share/nginx/html/
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/

# Nginx listens on port 80 by default
EXPOSE 80

# Default nginx entrypoint/cmd already serves the content — no override needed
