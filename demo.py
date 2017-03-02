def make_demo(keygen, prover, verifier):
    print('='*80)
    gen = keygen()
    print('running keygen...')
    peggy = prover(gen.generate_key())
    victor = verifier(peggy.public_key)
    message = 'Фед'
    print('signing...')
    signature = peggy.sign(message)
    print('verifying...')
    victor.verify(message, signature)
    print('=' * 80)
    return {
        'demo': locals(),
        'gen': gen.steps,
        'sign': peggy.steps,
        'verify': victor.steps
    }
