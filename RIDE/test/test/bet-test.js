const wvs = 10 ** 8;
const Seed = "stool tunnel test mind emotion identify orbit salt loud bitter various bronze evolve nut regular";
describe('bet test suite', async function () {
    this.timeout(100000);
    it('Can makeBet', async function () {
        const iTxBet10 = invokeScript({
            dApp: address("3MrC1oqVCoLkfHabhJtrLJS6GxcooQwRWuP"),
            call: {
                function: "bet",
                args: [{type:'integer', value: 1}]
                },
            payment: [{assetId: null, amount: 10}]
        }, Seed);
        const iTxBet20 = invokeScript({
            dApp: address("3MrC1oqVCoLkfHabhJtrLJS6GxcooQwRWuP"),
            call: {
                function: "bet",
                args: [{type:'integer', value: 2}]
                },
            payment: [{assetId: null, amount: 10}]
        }, Seed);
        await broadcast(iTxBet10);
        await waitForTx(iTxBet10.id);
        await broadcast(iTxBet20);
        await waitForTx(iTxBet20.id);
    })
})