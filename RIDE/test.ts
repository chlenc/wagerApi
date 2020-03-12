import { data, IDataEntry, IDataTransaction, massTransfer, setScript, WithId } from "@waves/waves-transactions";
import { address, randomSeed } from '@waves/ts-lib-crypto'
import { compile } from "@waves/ride-js";
import * as fs from 'fs';
import { broadcastAndWaitTx } from "./utils";



const getScriptLottery = require("./src/lotteryContract");
const getScriptHub = require("./src/hubContract");

const
    mrtAssetId = '4uK8i4ThRGbehENwa6MxyLtxAjAo1Rj9fduborGExarC',
    nodeUrl = 'https://nodes.wavesnodes.com',
    ticketPrice = 100,
    replenishAmount = 1000000,
    lotteryInfo: IAccountLottery[] = [];

interface IAccount {
    address: string
    seed: string
}

interface IAccountLottery extends IAccount {
    sum: number
}

(async () => {
    const hub: IAccount = {address: addressHub, seed: seedHub};
    //create Accounts
    ([{sum: 500, length: 12}, {sum: 1000, length: 6}, {sum: 2000, length: 4}] as { sum: number, length: number }[])
    //([{sum: 500, length: 4}, {sum: 1000, length: 1}, {sum: 2000, length: 1}] as { sum: number, length: number }[])
        .forEach(({sum, length}) => {
            Array.from({length}, (_, i) => i).forEach(() => {
                const seedLottery = randomSeed();
                const addressLottery = address(seedLottery, 'T');
                let lottery = {sum, address: addressLottery, seed: seedLottery};
                lotteryInfo.push(lottery)
            })
        });
    console.log('Accounts was created');

    //accrual of money on accounts
    await broadcastAndWaitTx(massTransfer({
        transfers: lotteryInfo
            .map((({address: recipient}) => ({
                recipient,
                amount: recipient === addressHub ? replenishAmount + 600000 * 4 : replenishAmount
            })))
    }, seedWithMoney));
    console.log('Money transfer to accounts successfully');

    //compile hub dApp and set script
    const compiledHub = compile(getScriptHub(mrtAssetId, ticketPrice));
    if (!('result' in compiledHub)) throw 'incorrect hub dApp';
    await broadcastAndWaitTx(setScript({script: compiledHub.result.base64, chainId: 'W'}, seedHub));
    console.log("Hub successfully scripted");


    //compile lottery dApp and set script
    const compiledLottery = compile(getScriptLottery(addressHub, addressAdminLottery, addressRandomizer, addressOwner));
    if (!('result' in compiledLottery)) throw 'incorrect lottery dApp';
    for (const {address, seed} of lotteryInfo) {
        await broadcastAndWaitTx(setScript({script: compiledLottery.result.base64, chainId: 'W'}, seed));
        console.log(`Lottery ${address} successfully scripted`);
    }
    console.log("All lotteries successfully scripted");

    //register lotteries in hub
    await broadcastAndWaitTx(data({
        data: lotteryInfo.map(({address}) => ({ key: "lottery_" + address, value: true})), fee: 600000
    }, seedHub));
    console.log("All lotteries successfully registered in hub");

    // turn on ticketing period
    await broadcastAndWaitTx(data({
        data: [{key: "status", value: "ticketingPeriod"}], fee: 600000
    }, seedHub));
    console.log("Ticketing period successfully turned on");

    //save files
    fs.writeFileSync("./src/hubInfo.json", JSON.stringify(hub, null, 4));
    fs.writeFileSync("./src/lotteryInfo.json", JSON.stringify(lotteryInfo, null, 4));
    fs.writeFileSync("../../lottery/src/json/constants.json",
        JSON.stringify({hubAddress: hub.address, mrtAssetId, nodeUrl, ticketPrice, pollInterval: 5}));
    fs.writeFileSync("../../lottery/src/json/lotteries.json", JSON.stringify(lotteryInfo.map(({address, sum}) => ({
        address,
        sum
    }))));
    console.log('files saved')
})();

