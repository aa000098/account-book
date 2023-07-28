import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { MoneybookLambdaStack } from './stack/lambda-stack';
import { MoneybookS3Stack } from './stack/s3-stack';
import { Account } from './config/accounts';
import { SYSTEM_NAME } from "./config/commons";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

// MoneybookStack의 속성을 정의하는 인터페이스
export interface MoneybookStackProps extends cdk.StackProps {
  context: Account
  s3Stack?: MoneybookS3Stack
}

// MoneybookStack 클래스 정의
export class MoneybookStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MoneybookStackProps) {
    // cdk.Stack 클래스의 생성자 호출
    super(scope, id, props);

    // MoneybookS3Stack 인스턴스 생성과 관련된 코드
    const s3Stack = new MoneybookS3Stack(this, `${SYSTEM_NAME}-s3Stack`, props);

    // MoneybookS3Stack 인스턴스를 MoneybookStack 속성에 할당
    // 람다스택에서 s3스택을 사용하므로 props에 할당해준 것임
    props.s3Stack = s3Stack;

    // MoneybookLambdaStack 인스턴스 생성
    new MoneybookLambdaStack(this, `${SYSTEM_NAME}-lambdaStack`, props)
  }
}
