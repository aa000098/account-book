export interface Account {
    readonly accountID: string;
    readonly region: string;
    readonly stage: string;
    readonly airportCode: string;
}

export const Accounts: Account[] = [
    {
        accountID: '879158308066',
        region: 'ap-northeast-2',
        stage: 'son-hyunho',
        airportCode: 'ICN',
    }
];

export function getAccountUniqueName(account: Account): string{
    return getAccountUniqueNameWithDelimiter(account, '-')
}

export function getAccountUniqueNameWithDelimiter(account: Account, delimiter: string): string{
    return '${account.stage}${delimiter}${account.airportCode}'
}

export function getDevAccount(userID: string): Account | undefined {
    return Accounts.find((account: Account) => { return account.stage === userID})
}