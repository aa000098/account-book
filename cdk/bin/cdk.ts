#!/usr/bin/env node
// Node.js 스크립트를 실행할 때 사용되는 시놀리지 선언(Shebang)

import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { MoneybookStack } from '../lib/moneybook-stack';
import { getAccountUniqueName, getDevAccount } from '../lib/config/accounts';
import * as os from 'os'

// CDK 애플리케이션 생성
const app = new cdk.App();

// 유저 이름 받아오기
let userName = os.userInfo().username
console.log(userName);

// 스택 이름 만들 때 쓰일 devAccount을 lib/config/accounts.ts 파일의
// getDevAccount 함수를 통해 만듦
const devAccount = getDevAccount(userName);
if (devAccount !== undefined) {
    // MoneybookStack 인스턴스 생성
    // lib/config/accounts.ts 파일의 getAccountUniqueName함수로 스택 이름 생성
    new MoneybookStack(app, `${getAccountUniqueName(devAccount)}`, {
        env: devAccount,
        context: devAccount,
    });
}

app.synth();