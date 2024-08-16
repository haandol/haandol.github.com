ARG RUBY_VERSION=3.3
FROM ruby:$RUBY_VERSION

RUN apt-get update \
  && apt-get install -y \
    git \
    locales \
    make \
    nodejs

WORKDIR /src

COPY . /src

RUN \
  bundle config local.github-pages /src && \
  NOKOGIRI_USE_SYSTEM_LIBRARIES=true bundle install --gemfile=/src/Gemfile

RUN \
  echo "ko_KR UTF-8" > /etc/locale.gen && \
  locale-gen ko-KR.UTF-8

ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

CMD ["jekyll", "serve", "-H", "0.0.0.0", "-P", "4000"]
