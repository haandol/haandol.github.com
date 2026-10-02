FROM mcr.microsoft.com/devcontainers/ruby:1-3.4-bookworm

# Refresh the image's Yarn signing key before Features run apt-get update.
RUN curl --fail --silent --show-error --location \
      https://dl.yarnpkg.com/debian/pubkey.gpg --output /tmp/yarn-pubkey.gpg \
    && gpg --batch --yes --dearmor \
      --output /usr/share/keyrings/yarn-archive-keyring.gpg /tmp/yarn-pubkey.gpg \
    && rm /tmp/yarn-pubkey.gpg
