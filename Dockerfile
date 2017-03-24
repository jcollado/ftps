FROM jcollado/python-ci:0.1
RUN apk add --no-cache gcc libc-dev python2-dev python3-dev curl-dev
CMD ["/bin/sh"]
