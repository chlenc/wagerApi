// Wallet.ride deploy script. To run execute `surfboard run path/to/script`

// wrap out script with async function to use fancy async/await syntax
(async () => {
    // Functions, available in tests, also available here
    const script = compile(file('../ride/bet.ride'));

    // You can set env varibles via cli arguments. E.g.: `surfboard run path/to/script  --variables 'dappSeed=seed phrase,secondVariable=200'`
    const dappSeed = "saasfasfasfas fasaf afs  asfa s";
    const dappAddress = "3Mu7V7BTQdkPGTNfLjVQzj96V32k7bsJWE1"
    const playerSeed = "asfas asf as fas fas afsa safs"

    if (dappSeed == null){
        throw new Error(`Please provide dappSedd`)
    }
    //const dappSeed = env.SEED; // Or use seed phrase from surfboard.config.json
    const ssTx = setScript({
        script,
        additionalFee: 400000 // Uncomment to raise fee in case of redeployment
    }, dappSeed);
    await broadcast(ssTx);
    await waitForTx(ssTx.id);

    console.log(ssTx.id);

    const params = {
        call: {
            args: [{type:'integer', value: 1}],
        function: 'bet',
        },
        payment: [{
        amount: 50,
        assetId: null
        }],
        dApp: dappAddress,
        chainId: 'T',
        fee: 500000,
        //senderPublicKey: 'by default derived from seed',
        //timestamp: Date.now(),
        //fee: 100000,
        //chainId:
      }
    const iTxBet10 = invokeScript(params, playerSeed)
    await broadcast(iTxBet10);
    await waitForTx(iTxBet10.id);
    console.log(iTxBet10);
})();
