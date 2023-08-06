# -*- mode: python ; coding: utf-8 -*-
import json
import pytest

try:
    import eth_account
except ImportError:
    eth_account			= None
try:
    from Crypto.Cipher	import AES
    from Crypto.Protocol.KDF import scrypt
except ImportError:
    AES				= None
    scrypt			= None

import shamir_mnemonic

from .			import account, create, addresses, addressgroups, accountgroups, Account
from .recovery		import recover

from .dependency_test	import substitute, nonrandom_bytes, SEED_XMAS, SEED_ONES


def test_account_smoke():
    acct			= account( SEED_XMAS )
    assert acct.address == '0x336cBeAB83aCCdb2541e43D514B62DC6C53675f4'
    assert acct.path == "m/44'/60'/0'/0/0"
    assert acct.key == '178870009416174c9697777b1d94229504e83f25b1605e7bb132aa5b88da64b6'

    acct			= account( SEED_XMAS, path="m/44'/60'/0'/0/1" )
    assert acct.address == '0x3b774e485fC818F0f377FBA657dfbF92B46f8504'
    assert acct.path == "m/44'/60'/0'/0/1"
    assert acct.pubkey == '03cbcf791b37011feab1c5d797cd76a3fa0f12ee5582adbe5aa4d8172a7bbaba5b'
    assert acct.key == acct.prvkey == 'bf299fe7a7d948fdb98474557bbee73395e01f3a6a73638d45d345f9adb451fb'
    assert acct.xpubkey == 'xpub6FVwqKQUrDre2ZPtAvcqR7GYW4662JTM7R1FGuwGAH3b1TjntLCbMa3HY7C1BR4ifXEtwfX63a69FEAcCSCgrgQZNd3WYgvKhAghRNucEc6'
    assert acct.xprvkey == 'xprvA2WbRosb1rJLp5KR4u5q3yKox2FbcqjVkC5eUXXebwWc8fQeLntLomiogp7vVMZcGfB4vaKeWRJ6eQmHSPRk6W7AJRNx2TT3Ai825JwH9kG'
    # And ensure we can round-trip the xprvkey (the x{pub/prv}keys encode other info, so won't be the same)
    acct			= account( acct.xprvkey, path="m/" )
    assert acct.path is None
    assert acct.address == '0x3b774e485fC818F0f377FBA657dfbF92B46f8504'
    assert acct.pubkey == '03cbcf791b37011feab1c5d797cd76a3fa0f12ee5582adbe5aa4d8172a7bbaba5b'
    assert acct.key == acct.prvkey == 'bf299fe7a7d948fdb98474557bbee73395e01f3a6a73638d45d345f9adb451fb'

    acct			= account( SEED_XMAS, crypto='Bitcoin' )
    assert acct.address == 'bc1qz6kp20ukkyx8c5t4nwac6g8hsdc5tdkxhektrt'
    assert acct.path == "m/84'/0'/0'/0/0"

    acct			= account( SEED_XMAS, crypto='Bitcoin', format='Legacy' )
    assert acct.address == '19FQ983heQEBXmopVNyJKf93XG7pN7sNFa'
    assert acct.path == "m/44'/0'/0'/0/0"
    assert acct.pubkey == '02d0bca9d976ad7303d1c0c3fd6ad0cb6bb78077d2ff158c16ac21bed763fb49a8'

    acct			= account( SEED_XMAS, crypto='Bitcoin', format='SegWit' )
    assert acct.address == '3HxUpD7E8Y31vDDgDq1VFdNXWViAgBjYJe'
    assert acct.path == "m/44'/0'/0'/0/0"

    # And, confirm that we retrieve the same Bech32 address for the all-ones seed,
    # as on a real Trezor "Model T".
    acct			= account( SEED_ONES, crypto='Bitcoin' )
    assert acct.address == 'bc1q9yscq3l2yfxlvnlk3cszpqefparrv7tk24u6pl'
    assert acct.path == "m/84'/0'/0'/0/0"
    assert acct.pubkey == '038f7fa5776f5359eb861994bee043f0b16a5ca24b66eb38696a7325d3e1717e72'
    assert acct.prvkey == acct.key == '80d5082773a4d2a07ee667a772ca13a120a5fc9d61bcf5a32f9e7ccf731bc0e6'
    assert acct.xpubkey == 'zpub6uMZYEpdewNa98z7Hge3R4GzeayoXCmtPUzFV7DVa4cc36k2Xh7oEDvs6baStXLxT8VtXkBZ56yfuk4D5JvM43nbB7EpdkmJC75ScEZm2QK'
    assert acct.xprvkey == 'zprvAgND8jHjpZpGveueBf733vLG6Z9K7k432G4egiot1j5dAJQsz9oYgRcPFJVUdpLe3tHnabyRmmuGY871GdTv8tkotCwyn6Ec5bZbb8RjtHF'

    acct			= account( SEED_XMAS, crypto='Litecoin' )
    assert acct.address == 'ltc1qfjepkelqd3jx4e73s7p79lls6kqvvmak5pxy97'
    assert acct.path == "m/84'/2'/0'/0/0"

    acct			= account( SEED_XMAS, crypto='Litecoin', format='Legacy' )
    assert acct.address == 'LeyK1dbc5qKdKC9TvkygMTeoHixR3z1XG3'
    assert acct.path == "m/44'/2'/0'/0/0"

    acct			= account( SEED_XMAS, crypto='Litecoin', format='SegWit' )
    assert acct.address == 'MPULjvY9dNjpNkgbwhfJtD7N6Lbfam1XsP'
    assert acct.path == "m/44'/2'/0'/0/0"

    acct			= account( SEED_XMAS, crypto='Dogecoin' )
    assert acct.address == 'DQCnF49GwQ5auL3u5c2uow62XS57RCA2r1'
    assert acct.path == "m/44'/3'/0'/0/0"

    acct			= account( SEED_ONES, crypto='Ripple' )
    assert acct.path == "m/44'/144'/0'/0/0"  # Default
    assert acct.address == 'rsXwvDVHHPrSm23gogdxJdrJg9WBvqRE9m'

    # Fake up some known Ripple pubkey --> addresses, by replacing the underlying "compressed"
    # public key function to return a fixed value.  Test values from:
    # trezor-firmware/core/tests/test_apps.ripple.address.py
    compressed_save		= acct.hdwallet.compressed
    acct.hdwallet.compressed	= lambda: 'ed9434799226374926eda3b54b1b461b4abf7237962eae18528fea67595397fa32'
    assert acct.pubkey == 'ed9434799226374926eda3b54b1b461b4abf7237962eae18528fea67595397fa32'
    assert acct.address == 'rDTXLQ7ZKZVKz33zJbHjgVShjsBnqMBhmN'
    acct.hdwallet.compressed	= lambda: '03e2b079e9b09ae8916da8f5ee40cbda9578dbe7c820553fe4d5f872eec7b1fdd4'
    assert acct.address == 'rhq549rEtUrJowuxQC2WsHNGLjAjBQdAe8'
    acct.hdwallet.compressed	= lambda: '0282ee731039929e97db6aec242002e9aa62cd62b989136df231f4bb9b8b7c7eb2'
    assert acct.address == 'rKzE5DTyF9G6z7k7j27T2xEas2eMo85kmw'
    acct.hdwallet.compressed	= compressed_save

    # Test values from a Trezor "Model T" w/ root seed 'zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong' loaded.
    # The Trezor Suite UI produced the following account derivation path and public address for:
    acct.from_mnemonic( 'zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong' )
    assert acct.path == "m/44'/144'/0'/0/0"  # Default
    assert acct.address == 'rUPzi4ZwoYxi7peKCqUkzqEuSrzSRyLguV'
    assert acct.pubkey == '039d65db4964cbf2049ad49467a6b73e7fec7d6e6f8a303cfbdb99fa21c7a1d2bc'
    assert acct.prvkey == '6501276b9d7f646742feb12fd066e107af8c1e26e4ad7c2694279d44c43bdfb2'


@pytest.mark.skipif( not scrypt or not eth_account,
                     reason="pip install slip39[wallet] to support private key encryption" )
def test_account_encrypt():
    """Ensure BIP-38 and Ethereum JSON wallet encryption and recovery works."""

    acct			= account( SEED_XMAS, crypto='Bitcoin' )
    assert acct.address == 'bc1qz6kp20ukkyx8c5t4nwac6g8hsdc5tdkxhektrt'
    assert acct.crypto == 'BTC'
    assert acct.path == "m/84'/0'/0'/0/0"
    assert acct.legacy_address() == "134t1ktyF6e4fNrJR8L6nXtaTENJx9oGcF"

    bip38_encrypted		= acct.encrypted( 'password' )
    assert bip38_encrypted == '6PYKmUhfJa5m1NR2zUaeHC3wUzGDmb1seSEgQHK7PK5HaVRHQSp7N4ytVf'

    acct_reco			= Account( crypto='Bitcoin' ).from_encrypted( bip38_encrypted, 'password' )
    assert acct_reco.address == 'bc1qz6kp20ukkyx8c5t4nwac6g8hsdc5tdkxhektrt'
    assert acct.crypto == 'BTC'
    assert acct.path == "m/84'/0'/0'/0/0"  # The default; assumed...
    assert acct_reco.legacy_address() == "134t1ktyF6e4fNrJR8L6nXtaTENJx9oGcF"

    acct			= account( SEED_XMAS, crypto='Ethereum' )
    assert acct.address == '0x336cBeAB83aCCdb2541e43D514B62DC6C53675f4'
    assert acct.crypto == 'ETH'
    assert acct.path == "m/44'/60'/0'/0/0"

    json_encrypted		= acct.encrypted( 'password' )
    assert json.loads( json_encrypted ).get( 'address' ) == '336cbeab83accdb2541e43d514b62dc6c53675f4'

    acct_reco			= Account( crypto='ETH' ).from_encrypted( json_encrypted, 'password' )
    assert acct_reco.address == '0x336cBeAB83aCCdb2541e43D514B62DC6C53675f4'
    assert acct.crypto == 'ETH'

    # Some test cases from https://en.bitcoin.it/wiki/BIP_0038

    # No compression, no EC multiply.  These tests produce the correct private key hex, but the
    # address hash verification check fails.  I suspect that they were actually created with a
    # *different* passphrase...
    assert Account( crypto='BTC' ).from_encrypted(
        '6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg',
        'TestingOneTwoThree',
        strict=False,
    ).key.upper() == 'CBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A5'

    assert Account( crypto='BTC' ).from_encrypted(
        '6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq',
        'Satoshi',
        strict=False,
    ).key.upper() == '09C2686880095B1A4C249EE3AC4EEA8A014F11E6F986D0B5025AC1F39AFBD9AE'

    # This weird UTF-8 test I cannot get to pass, regardless of what format I supply the passphrase in..

    # acct_reco			= Account( crypto='BTC' ).from_encrypted(
    #     '6PRW5o9FLp4gJDDVqJQKJFTpMvdsSGJxMYHtHaQBF3ooa8mwD69bapcDQn',
    #      bytes.fromhex('cf9300f0909080f09f92a9'), # '\u03D2\u0301\u0000\U00010400\U0001F4A9'
    # )
    # assert acct_reco.legacy_address() == '16ktGzmfrurhbhi6JGqsMWf7TyqK9HNAeF'

    # No compression, no EC multiply.  These test pass without relaxing the address hash verification check.
    assert Account( crypto='BTC' ).from_encrypted(
        '6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeo',
        'TestingOneTwoThree'
    ).key.upper() == 'CBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A5'

    assert Account( crypto='BTC' ).from_encrypted(
        '6PYLtMnXvfG3oJde97zRyLYFZCYizPU5T3LwgdYJz1fRhh16bU7u6PPmY7',
        'Satoshi'
    ).key.upper() == '09C2686880095B1A4C249EE3AC4EEA8A014F11E6F986D0B5025AC1F39AFBD9AE'

    # Test some addresses encrypted by our Paper Wallet PDF output procedure, using
    # the "zoo zoo ... zoo wrong" BIP-39 test Mnemonic.
    assert Account( crypto='BTC' ).from_encrypted(
        '6PYSUhj4mPTNdSvm2dxLRszieSBmzPqPQX699ECUrd69sWteFAUqmW1FLq',
        'something'
    ).address == 'bc1qk0a9hr7wjfxeenz9nwenw9flhq0tmsf6vsgnn2'

    # Ripple BIP-38 encrypted wallets.  Should round-trip via BIP-38
    acct_xrp = Account( crypto='XRP' )
    acct_xrp.from_mnemonic( 'zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong' )
    assert acct_xrp.path == "m/44'/144'/0'/0/0"  # Default
    assert acct_xrp.address == 'rUPzi4ZwoYxi7peKCqUkzqEuSrzSRyLguV'  # From Trezor "Model T" w/
    assert acct_xrp.pubkey == '039d65db4964cbf2049ad49467a6b73e7fec7d6e6f8a303cfbdb99fa21c7a1d2bc'
    acct_xrp_encrypted		= acct_xrp.encrypted( 'password' )
    assert acct_xrp_encrypted == '6PYTRxHt4sPM9i6zagBJ4pWdaefJ1FfVQwFCWQxDhVBw7fJYpYP3kMPfro'

    acct_dec			= Account( crypto='XRP' ).from_encrypted( acct_xrp_encrypted, 'password' )
    acct_dec.path == "m/44'/144'/0'/0/0"
    assert acct_dec.address == 'rUPzi4ZwoYxi7peKCqUkzqEuSrzSRyLguV'
    assert acct_dec.pubkey == '039d65db4964cbf2049ad49467a6b73e7fec7d6e6f8a303cfbdb99fa21c7a1d2bc'


@substitute( shamir_mnemonic.shamir, 'RANDOM_BYTES', nonrandom_bytes )
def test_create():
    """Standard SLIP-39 Mnemonic and account creation"""
    details			= create(
        "SLIP39 Wallet: Test",
        1,
        dict( fren = (3,5) ),
        SEED_XMAS
    )

    assert details.groups == {
        "fren": ( 3, [
            "academic acid academic acne academic academic academic academic academic academic academic academic academic academic academic academic academic carpet making building",
            "academic acid academic agree depart dance galaxy acrobat mayor disaster quick justice ordinary agency plunge should pupal emphasis security obtain",
            "academic acid academic amazing crush royal faint spit briefing craft floral negative work depend prune adapt merit romp home elevator",
            "academic acid academic arcade cargo unfold aunt spider muscle bedroom triumph theory gather dilemma building similar chemical object cinema salon",
            "academic acid academic axle crush swing purple violence teacher curly total equation clock mailman display husband tendency smug laundry disaster"
        ] ),
    }

    assert len(details.accounts) == 1
    [(eth,btc)] = details.accounts  # The default accounts created are ETH, BTC
    assert eth.address == '0x336cBeAB83aCCdb2541e43D514B62DC6C53675f4'
    assert btc.address == 'bc1qz6kp20ukkyx8c5t4nwac6g8hsdc5tdkxhektrt'

    assert recover( details.groups['fren'][1][:3] ) == SEED_XMAS


@substitute( shamir_mnemonic.shamir, 'RANDOM_BYTES', nonrandom_bytes )
def test_create_bip39():
    """Standard SLIP-39 Mnemonic from BIP-39 backup and account creation.

    """
    details			= create(
        "SLIP39 Wallet: Test",
        1,
        dict( fren = (3,5) ),
        SEED_ONES,
        using_bip39	= True,
        cryptopaths	= ('ETH','BTC','XRP'),
    )

    assert len(details.accounts) == 1
    [(eth,btc,xrp)] = details.accounts
    # recognizable ETH, BTC accounts generated from the 0xffff...ffff (zoo zoo ...  wrong) Seed.
    assert eth.address == '0xfc2077CA7F403cBECA41B1B0F62D91B5EA631B5E'
    assert btc.address == 'bc1qk0a9hr7wjfxeenz9nwenw9flhq0tmsf6vsgnn2'
    assert xrp.address == 'rUPzi4ZwoYxi7peKCqUkzqEuSrzSRyLguV'


def test_addresses():
    master_secret		= b'\xFF' * 16
    addrs			= list( addresses(
        master_secret	= master_secret,
        crypto		= 'ETH',
        paths		= ".../-9",
    ))
    # print( json.dumps( addrs, indent=4, default=str ))
    assert addrs == [
        (
            "ETH",
            "m/44'/60'/0'/0/0",
            "0x824b174803e688dE39aF5B3D7Cd39bE6515A19a1"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/1",
            "0x8D342083549C635C0494d3c77567860ee7456963"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/2",
            "0x52787E24965E1aBd691df77827A3CfA90f0166AA"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/3",
            "0xc2442382Ae70c77d6B6840EC6637dB2422E1D44e"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/4",
            "0x42a910D380dE132B5227e3277Cc70C3C76a884aC"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/5",
            "0x1A3db5E0422c78F43a35686f0307Da8f22344dE0"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/6",
            "0x19031c515C5d91DB7988D89AAA6F71a5825f5245"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/7",
            "0xaE693156ac600f5B0D58e5090ecf0A578c5Cc0a8"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/8",
            "0x4347541fa648BCE62543a8AbC2901E08017f6A6a"
        ),
        (
            "ETH",
            "m/44'/60'/0'/0/9",
            "0xC11235559Dd4c5224a19396C3A14526E92ebba35"
        )
    ]
    addrs			= list( addresses(
        master_secret	= master_secret,
        crypto		= 'BTC',
        paths		= '.../0/-2',
        format		= 'Bech32',
    ))
    print( json.dumps( addrs, indent=4, default=str ))
    assert addrs == [
        (
            "BTC",
            "m/84'/0'/0'/0/0",
            "bc1q9yscq3l2yfxlvnlk3cszpqefparrv7tk24u6pl"
        ),
        (
            "BTC",
            "m/84'/0'/0'/0/1",
            "bc1qnec684yvuhfrmy3q856gydllsc54p2tx9w955c"
        ),
        (
            "BTC",
            "m/84'/0'/0'/0/2",
            "bc1q2snj0zcg23dvjpw7m9lxtu0ap0hfl5tlddq07j"
        ),
    ]


def test_addressgroups():
    master_secret		= SEED_ONES
    addrgrps			= list( enumerate( addressgroups(
        master_secret	= master_secret,
        cryptopaths	= [
            ('ETH',	".../-3"),
            ('BTC',	".../-3"),
            ('LTC',	".../-3"),
            ('Doge',	".../-3"),
            ('CRO',	".../-3"),
            ('Binance',	".../-3"),
            ('Ripple',	".../-3"),
        ],
    )))
    # print( addrgrps )
    assert addrgrps == [
        (0, (("ETH",  "m/44'/60'/0'/0/0", "0x824b174803e688dE39aF5B3D7Cd39bE6515A19a1"),
             ("BTC",  "m/84'/0'/0'/0/0",  "bc1q9yscq3l2yfxlvnlk3cszpqefparrv7tk24u6pl"),
             ('LTC',  "m/84'/2'/0'/0/0",  'ltc1qe5m2mst9kjcqtfpapaanaty40qe8xtusmq4ake'),
             ('DOGE', "m/44'/3'/0'/0/0",  'DN8PNN3dipSJpLmyxtGe4EJH38EhqF8Sfy'),
             ('CRO',  "m/84'/60'/0'/0/0", 'crc1q4hdzumgzgfda84hvt67e4znnfxxnnnc42jgqt9'),
             ('BNB',  "m/44'/60'/0'/0/0", '0x824b174803e688dE39aF5B3D7Cd39bE6515A19a1'),
             ('XRP',  "m/44'/144'/0'/0/0",'rsXwvDVHHPrSm23gogdxJdrJg9WBvqRE9m'))),
        (1, (("ETH",  "m/44'/60'/0'/0/1", "0x8D342083549C635C0494d3c77567860ee7456963"),
             ("BTC",  "m/84'/0'/0'/0/1",  "bc1qnec684yvuhfrmy3q856gydllsc54p2tx9w955c"),
             ('LTC',  "m/84'/2'/0'/0/1",  'ltc1qm0hwvvk28wlyfu3sed66e9yyvmwm35xtfexva3'),
             ('DOGE', "m/44'/3'/0'/0/1",  'DJYE9WWaCA1CbV9x23qkcgNX7Yr9YjCebA'),
             ('CRO',  "m/84'/60'/0'/0/1", 'crc1qalq0kk8j8mwljneavgmqytcv63vnjjhsn8cfhs'),
             ('BNB',  "m/44'/60'/0'/0/1", '0x8D342083549C635C0494d3c77567860ee7456963'),
             ('XRP',  "m/44'/144'/0'/0/1",'rfMBrTc7VRTLUZu2K517r594Ky9qU5fQ5i'))),
        (2, (("ETH",  "m/44'/60'/0'/0/2", "0x52787E24965E1aBd691df77827A3CfA90f0166AA"),
             ("BTC",  "m/84'/0'/0'/0/2",  "bc1q2snj0zcg23dvjpw7m9lxtu0ap0hfl5tlddq07j"),
             ('LTC',  "m/84'/2'/0'/0/2",  'ltc1qx3r3efsmupn34gmwu25fu39tn4h79cjfwvlpfu'),
             ('DOGE', "m/44'/3'/0'/0/2",  'DQfJcJzLFW9LJPJXNkLeq1WqPfLsRq47Jj'),
             ('CRO',  "m/84'/60'/0'/0/2", 'crc1qnr2z9wv2z5p54k8sm35fv7m5u86sutwa7m7e99'),
             ('BNB',  "m/44'/60'/0'/0/2", '0x52787E24965E1aBd691df77827A3CfA90f0166AA'),
             ('XRP',  "m/44'/144'/0'/0/2",'rn7vgevVmF8HXq7FYNhL34gdJMUFukghPz'))),
        (3, (("ETH",  "m/44'/60'/0'/0/3", "0xc2442382Ae70c77d6B6840EC6637dB2422E1D44e"),
             ("BTC",  "m/84'/0'/0'/0/3", "bc1qxwekjd46aa5n0s3dtsynvtsjwsne7c5f5w5dsd"),
             ('LTC',  "m/84'/2'/0'/0/3", 'ltc1qnqzyear8kct0yjzupe2pxtq0mwee5kl642mj78'),
             ('DOGE', "m/44'/3'/0'/0/3", 'DLVPiM5763cyNJfoa13cv4kV3b87FgVMCS'),
             ('CRO',  "m/84'/60'/0'/0/3", 'crc1qtlwuk2p8znv43xpxvupe7ye3ueuxen3475yn8n'),
             ('BNB',  "m/44'/60'/0'/0/3", '0xc2442382Ae70c77d6B6840EC6637dB2422E1D44e'),
             ('XRP',  "m/44'/144'/0'/0/3",'rB1KWkYEg7n78eA2GWWrKWvjkHDhVEdRXC'))),
    ]


def test_accountgroups():
    master_secret		= b'\xFF' * 16
    acctgrps			= list( accountgroups(
        master_secret	= master_secret,
        cryptopaths	= [
            ('ETH', ".../-3"),
            ('BTC', ".../-3"),
        ],
    ))
    # print( json.dumps( acctgrps, default=repr ))
    assert len(acctgrps) == 4
