The document to split into keyshares should be mounted into the `/app/split` directory of the container. The resulting keyshare files to distribute will appear next to it once the container terminates.

```
docker run --rm -it -v "${PWD}/split/:/app/split/" captainkark/secretsharing:9b29721 split /app/split/foobar.txt
```

Afterwards, on the host machine:

```
$: ls -A1 split/
foobar.txt
foobar-1
foobar-2
foobar-3
foobar-4
foobar-5
```

### Recovering

Copy in enough keyshares to regenerate the original secret.

```
mv ./split/foobar-1 ./recover/
mv ./split/foobar-3 ./recover/
mv ./split/foobar-5 ./recover/
```

Point the recover script at the directory where the shards are located.

```
docker run --rm -it -v "${PWD}/recover/:/app/recover/" captainkark/secretsharing:9b29721 recover /app/recover/
```

The original secret will appear next to the shards once the container terminates.

```
$: ls -A1 recover/
secret
foobar-1
foobar-3
foobar-5
```
