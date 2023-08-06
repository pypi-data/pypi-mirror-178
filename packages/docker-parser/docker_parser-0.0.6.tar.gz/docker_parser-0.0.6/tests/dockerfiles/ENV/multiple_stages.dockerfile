FROM base as horcrux
ENV MY_NAME="John Doe"
FROM base as sacred_place
ENV MY_DOG=Rex\ The\ Dog \
    MY_CAT=fluffy
ENV ONE TWO= THREE=world
FROM base as nothing