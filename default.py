import argparse

from pathlib2 import Path

from secretsharing import (
    BitcoinToB32SecretSharer,
    BitcoinToB58SecretSharer,
    BitcoinToZB32SecretSharer,
    PlaintextToHexSecretSharer,
    SecretSharer,
    points_to_secret_int,
    secret_int_to_points
)

SPLIT_OPERATIONS = {
    'base32': BitcoinToB32SecretSharer.split_secret,
    'base58': BitcoinToB58SecretSharer.split_secret,
    'hex': SecretSharer.split_secret,
    'int': secret_int_to_points,
    'text': PlaintextToHexSecretSharer.split_secret,
    'zbase32':  BitcoinToZB32SecretSharer.split_secret
}

RECOVER_OPERATIONS = {
    'base32': BitcoinToB32SecretSharer.recover_secret,
    'base58': BitcoinToB58SecretSharer.recover_secret,
    'hex': SecretSharer.recover_secret,
    'int': points_to_secret_int,
    'text': PlaintextToHexSecretSharer.recover_secret,
    'zbase32':  BitcoinToZB32SecretSharer.recover_secret
}

def split(args, operation_fn):
    target, quorum, total = args.target, args.quorum, args.total
    shards = operation_fn(target.read_text().encode('ascii'), quorum, total)
    for i, shard in enumerate(shards):
        shard_file = target.with_name("{0}-{1}".format(
            target.stem,
            i,  # note: more than 10 won't sort right
        ))
        shard_file.write_text(unicode(shard), encoding='utf-8')


def recover(args, operation_fn):
    target, secret_file = args.target, args.secret_file
    shard_files = list(target.rglob('[!.gitignore]*'))
    shards = [s.read_text().encode('ascii') for s in shard_files]
    secret_file.write_text(unicode(operation_fn(shards)), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
            """Split or recover shares using shamir's secret sharing algorithm. """
            """Uses https://github.com/blockstack/secret-sharing to do this."""
        )
    )

    parser.add_argument(
        'operation',
        help="whether to split or to recover",
        choices=['split', 'recover'],
        type=str
    )

    parser.add_argument(
        'target',
        help=(
            """the file where the secret to split is, """
            """or the directory where the shares are to recover"""
        ),
        type=Path
    )

    parser.add_argument(
        '--quorum',
        help="total number of shares needed to regenerate the original secret",
        type=int,
        default=3
    )

    parser.add_argument(
        '--total',
        help="total number of shares to create",
        type=int,
        default=5
    )

    parser.add_argument(
        '--secret-type',
        help="data type of the raw secret value",
        type=str,
        default='text',
        choices=list(SPLIT_OPERATIONS.keys())
    )

    parser.add_argument(
        '--secret-file',
        help="if using 'recover', location to put the recovered secret file",
        type=Path,
        default='./recover/secret'
    )

    args = parser.parse_args()
    quorum, total, operation, secret_type = (
        args.quorum, args.total, args.operation, args.secret_type
    )

    if quorum < 1:
        raise SystemExit("Quorum must be greater than 1")

    if quorum > total:
        raise SystemExit("Quorum cannot be greater than total shares")

    if operation == 'split':
        split(args, SPLIT_OPERATIONS.get(secret_type))

    if operation == 'recover':
        recover(args, RECOVER_OPERATIONS.get(secret_type))
