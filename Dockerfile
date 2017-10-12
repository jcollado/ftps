FROM jcollado/python-ci:0.2
RUN apk add --no-cache curl-dev gcc libc-dev libffi-dev openssl-dev python2-dev python3-dev
CMD ["/bin/sh"]
